import msg_queue_assistance
import zscript

def main():
    msg_queue = msg_queue_assistance.msg_queue_assistance()
    asin_list=msg_queue.extract_queue_5_round()

    while len(asin_list)>0:
        scrape_object=zscript.zscript()
        asin_scraped, asin_not_scraped=scrape_object.run_scrape(asin_list)
        msg_queue.insert_msg_queue(asin_scraped)
        msg_queue.insert_daily_list_queue(asin_not_scraped)
        asin_list = msg_queue.extract_queue_5_round()



if __name__ == "__main__":
    main()