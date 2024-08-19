import scrapy
import json
import re
import random
from sqlalchemy.orm import sessionmaker
from ..hotel_model import Hotel, engine
import os
import requests
from urllib.parse import urljoin

class TripSpider(scrapy.Spider):
    name = 'trip_spider'
    start_urls = [
        'https://uk.trip.com/hotels/?locale=en-GB&curr=USD#ctm_ref=ih_h_6_1'
    ]
    def __init__(self, *args, **kwargs):
        super(TripSpider, self).__init__(*args, **kwargs)
        self.Session = sessionmaker(bind=engine)

    def parse(self, response):
        api_url = 'https://uk.trip.com/hotels/?locale=en-GB&curr=USD#ctm_ref=ih_h_6_1'  

        headers = {
            ':authority': 'uk.trip.com',
            ':method': 'GET',
            ':path':'/hotels/?locale=en-GB&curr=GBP',
            ':scheme':'https',
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Encoding':'gzip, deflate, br, zstd',
            'Accept-language':'en-GB,en-US;q=0.9,en;q=0.8',
            'Cache-Control':'max-age=0',
            'Cookie':'ibu_enable_nonessential=0; ibulanguage=EN; ibulocale=en_gb; cookiePricesDisplayed=GBP; UBT_VID=1723022910410.4bf4fp9kyqg5; _abtest_userid=cb9fc64f-bbd1-4ccf-bdf4-77d59ef2a0ab; devicePixelRatio=1; _gcl_au=1.1.1518663545.1723022916; _fwb=90ArTLYDEeGvsl7c6AV3CQ.1723022916773; _tt_enable_cookie=1; _ttp=XcM2dC7rLhIgwU5TmqOwK61P4lL; GUID=09031113212150362020; nfes_isSupportWebP=1; nfes_isSupportWebP=1; intl_ht1=h4%3D338_730568; _RF1=45.118.63.60; _RSG=WXq5b0EaPO1mN1_OwD6tg9; _RDG=2879592535d1d222450acbf869811bdbd7; _RGUID=161990e0-2517-4860-9ab7-18de98fc15f0; _ga_37RNVFDP1J=GS1.2.1723026090.2.1.1723026592.10.0.0; _ga_2DCSB93KS4=GS1.2.1723026090.2.1.1723026593.10.0.0; _ga_X437DZ73MR=GS1.1.1723028990.3.0.1723028990.0.0.0; _ga=GA1.2.193632688.1723022917; _gid=GA1.2.439346045.1723279852; g_state={"i_p":1723884657366,"i_l":3}; ibu_online_permission_cls_ct=2; ibu_online_permission_cls_gap=1723290829523; IBU_TRANCE_LOG_P=96686785943; _uetsid=09bbf5a0570f11ef9ec6370e8d9430b4; _uetvid=cfba741054a611efbd755bf49726a2d4; _bfa=1.1723022910410.4bf4fp9kyqg5.1.1723311191204.1723315353789.8.1.10320668150; wcs_bt=s_33fb334966e9:1723315356',
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Upgrade-Insecure-Requests": "1",
            "Sec-Gpc": "1", 
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Dest": "document",
            "Sec-Ch-Ua-Platform": "Linux",
            "Sec-Ch-Ua-Mobile": "?0",
            "Referer":"https://uk.trip.com/",
            "Priority":"u=0, i",
            'X-Requested-With': 'XMLHttpRequest'
        }

        payload = {
            'locale':'en-GB',
            'curr':'GBP'
        }

        yield scrapy.Request(
            url=api_url,
            method='GET',
            headers=headers,
            body=json.dumps(payload),
            callback=self.parse_ajax_response
        )

    def parse_ajax_response(self, response):
        script_content = response.xpath('//script[contains(., "window.IBU_HOTEL")]/text()').get()
        json_data = re.search(r'window\.IBU_HOTEL\s*=\s*({.*?});', script_content, re.DOTALL)

        if json_data:
            json_string = json_data.group(1)
            hotel_data = json.loads(json_string)

            all_sections = ['inboundCities', 'outboundCities', 'fiveStarHotels', 'cheapHotels', 'hostelHotels']
            chosen_sections = random.sample(all_sections, 3)
            
            self.logger.info(f"Randomly chosen sections: {chosen_sections}")

            for section in chosen_sections:
                if section in hotel_data['initData']['htlsData']:
                    self.process_section(hotel_data['initData']['htlsData'][section], section)
                else:
                    self.logger.info(f"Section {section} not found in the data.")

    def process_section(self, section_data, section_name):
        self.logger.info(f"Processing section: {section_name}")
        if section_name in ['inboundCities', 'outboundCities']:
            for city in section_data:
                city_name = city.get('name', 'Unknown City')
                for hotel in city.get('recommendHotels', []):
                    self.extract_hotel_info(hotel, city_name, section_name)
        else:
            for hotel in section_data:
                self.extract_hotel_info(hotel, 'N/A', section_name)

    def extract_hotel_info(self, hotel, city_name, section_name):
        hotel_data = {
            'hotel_id': hotel.get('hotelId'),
            'hotel_name': hotel.get('hotelName'),
            'hotel_url': hotel.get('hotelJumpUrl'),
            'hotel_location': hotel.get('fullAddress'),
            'latitude': hotel.get('lat'),
            'longitude': hotel.get('lon'),
            'rating': hotel.get('rating'),
            'price': hotel.get('prices', {}).get('priceInfos', [{}])[0].get('price'),
            'city': city_name if city_name != 'N/A' else None,
            'section': section_name
        }

        # Save image and get local file path
        image_url = f"https://ak-d.tripcdn.com/images{hotel.get('imgUrl')}"
        if image_url:
            local_image_path = self.save_image(image_url, hotel_data['hotel_id'])
            hotel_data['image_url'] = local_image_path  # Store local file path instead of URL

        session = self.Session()
        try:
            new_hotel = Hotel(**hotel_data)
            session.add(new_hotel)
            session.commit()
            self.logger.info(f"Saved hotel: {hotel_data['hotel_name']}")
        except Exception as e:
            session.rollback()
            self.logger.error(f"Error saving hotel: {e}")
        finally:
            session.close()

    def save_image(self, image_url, hotel_id):
        directory = 'images'
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        try:
            image_url = urljoin(self.start_urls[0], image_url)
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            
            filename = os.path.join(directory, f'{hotel_id}.jpg')
            with open(filename, 'wb') as f:
                f.write(response.content)
            
            self.logger.info(f"Image saved as: {filename}")
            return filename  # Return the local file path
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error downloading image {image_url}: {e}")
            return None



        









