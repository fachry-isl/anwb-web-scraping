import scrapy
from scrapy_playwright.page import PageMethod
from anwb_scrapy.items import AnwbScrapyItem
from anwb_scrapy.helper import get_fuel_type_bycarname, parse_car_manufacture, parse_car_model, parse_fuel_type, parse_chassis, parse_price
from playwright.async_api import async_playwright

class AnwbSpider(scrapy.Spider):
    name = 'anwb'
    
    def start_requests(self):
        # Start the scraping by requesting the main page
        yield scrapy.Request('https://www.anwb.nl/auto/private-lease/anwb-private-lease/aanbod/begin-bij=1000',
                meta=dict(
                    playwright=True,
                    playwright_include_page=True,
                    playwright_page_methods=[
                        PageMethod('wait_for_selector', 'div.sc-joEDEW.lnsMrA')
                    ]
                ))

    async def parse(self, response):
        # Parse the main page to extract basic car information
        for car in response.xpath("//div[@class='sc-joEDEW lnsMrA']/section/div"):
            item = AnwbScrapyItem()
            carname = car.xpath(".//span[@data-test='lease-car-tile-header-link-text']//text()").get()
            price = car.xpath(".//span[@data-test='price-text-xl']//text()").get()
            detailed_url = car.xpath(".//span[@data-test='lease-car-tile-header-link']/a[@href]/@href").get()
            
            item['carname'] = carname
            item['price'] = price
            item['detailed_url'] = detailed_url
            
            # Request details page for each car
            yield scrapy.Request(
                url=detailed_url,
                callback=self.parse_item_details,
                meta={'item': item}  # Pass the item to the callback method
            )
    
    async def parse_item_details(self, response):
        # Parse the details page to extract additional car information
        item = response.meta['item']
        chassis = response.xpath("(//ul[@data-test='list-list-unordered'])[2]/li[2]//text()").get()
        fuel_type = response.xpath("(//ul[@data-test='list-list-unordered'])[2]/li[6]//text()").get()
        
        # Handle cases where 'Transmissie' is mistakenly extracted as fuel type
        if "Transmissie:" in fuel_type:
            fuel_type = response.xpath("(//ul[@data-test='list-list-unordered'])[2]/li[7]//text()").get()
        
        # Handle variations in the HTML structure
        if "Carrosserie" not in chassis:
            try:
                # Use Playwright for dynamic content
                pw = await async_playwright().start()
                browser = await pw.chromium.launch(headless=True)
                page = await browser.new_page()
                
                await page.goto(item['detailed_url'], timeout=100000)
                # Wait for selector - third variation will fail here
                await page.wait_for_selector('div.sc-IqJVf.eHlScc', timeout=100000)
                
                # Extract chassis using Playwright
                xpath_expression = "//div[@class='sc-ePDLzJ fLzLfm PONCHO-description-list']//dd[5]//text()"
                chassis = await page.evaluate(f'document.evaluate("{xpath_expression}", document, null, XPathResult.STRING_TYPE, null).stringValue')

                # Extract fuel type using Playwright
                xpath_expression = "//div[@class='sc-ePDLzJ fLzLfm PONCHO-description-list']//dd[2]//text()"
                fuel_type = await page.evaluate(f'document.evaluate("{xpath_expression}", document, null, XPathResult.STRING_TYPE, null).stringValue')
                self.logger.info("SECOND VARIATION")
                
                item['chassis'] = chassis
                item['fuel_type'] = fuel_type
                    
            except Exception as e:    
                # Handle exceptions and try a revised approach for the third variation
                self.logger.error(f"Exception {e}")
                self.logger.info(f"THIRD VARIATION: {item['detailed_url']}")
                
                pw_2 = await async_playwright().start()
                browser_2 = await pw_2.chromium.launch(headless=True)
                page_2 = await browser_2.new_page()
                await page_2.goto(item['detailed_url'], timeout=100000)
                # Wait for selector
                await page_2.wait_for_selector('div.sc-joEDEW.lnsMrA', timeout=100000)
                # Revised detailed url
                xpath_expression = "//div[@class='sc-joEDEW lnsMrA']/section/div[1]//span[@data-test='lease-car-tile-header-link']/a[@href]/@href"
                detailed_url = await page_2.evaluate(f'document.evaluate("{xpath_expression}", document, null, XPathResult.STRING_TYPE, null).stringValue')
                
                # Use Playwright for the revised approach
                pw_detail = await async_playwright().start()
                browser_detail = await pw_detail.chromium.launch(headless=True)
                page_detail = await browser_detail.new_page()
                await page_detail.goto(detailed_url, timeout=100000)
                # Wait for selector
                await page_detail.wait_for_selector('div.sc-IqJVf.eHlScc', timeout=100000)
                
                # Extract chassis using Playwright
                xpath_expression = "//div[@class='sc-ePDLzJ fLzLfm PONCHO-description-list']//dd[5]//text()"
                chassis = await page_detail.evaluate(f'document.evaluate("{xpath_expression}", document, null, XPathResult.STRING_TYPE, null).stringValue')
                
                # Extract fuel type using Playwright
                xpath_expression = "//div[@class='sc-ePDLzJ fLzLfm PONCHO-description-list']//dd[2]//text()"
                fuel_type = await page_detail.evaluate(f'document.evaluate("{xpath_expression}", document, null, XPathResult.STRING_TYPE, null).stringValue')
                
                # Close the browser instances to free up resources
                await browser_2.close()
                await browser_detail.close()
                
                item['chassis'] = chassis
                item['fuel_type'] = fuel_type
            finally:
                # Close the browser instances to free up resources
                await browser.close()

                
        else:
            item['chassis'] = chassis
            item['fuel_type'] = fuel_type
        
        # Further processing and parsing (helper.py)
        item['manufacturer'] = await parse_car_manufacture(item)
        item['model'] = await parse_car_model(item)
        item['fuel_type'] = await parse_fuel_type(item)
        item['chassis'] = await parse_chassis(item)
        item['price'] = await parse_price(item)
        item['fuel_type'] = await get_fuel_type_bycarname(item)
           
        # Yield the final result
        yield {
            'Manufacturer': item['manufacturer'],
            'Model': item['model'],
            'Price': item['price'],
            'Fuel Type': item['fuel_type'],
            'Vehicle Chassis': item['chassis']
        }
