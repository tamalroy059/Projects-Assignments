import amazon_parser
import msg_queue_assistance

def main():

    msg_queue = msg_queue_assistance.msg_queue_assistance()
    msg_queue.change_round(1)
    parser=amazon_parser.amazon_parser()


    asin_list = msg_queue.extract_queue_5_round("dev-aws-python-already-scraped", attributes=['process_date', 'eisbn'])


    while len(asin_list)>0:
        for asin in asin_list:
            print asin
            file_name='amazon_page_%s_%s.txt'%(asin[0],asin[1])
            file_path=parser.move_from_s3_to_local(asin[1],file_name)
            if file_path is None:
                print asin
            else:
                parser.parser(file_path, asin)

        asin_list = msg_queue.extract_queue_5_round("dev-aws-python-already-scraped",
                                                    attributes=['process_date', 'eisbn'])





if __name__ == "__main__":
    main()