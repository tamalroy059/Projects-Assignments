import bottlenose
import xml.etree.ElementTree as ET


class amazon_api:

    def __init__(self, itemid):
        self.__amazon_product_advertising_api_extract(itemid)


    def __amazon_product_advertising_api_extract(self,itemid):

        key_access = 'AKIAIO6ZO7NXRZIL2M4A'
        key_secret = '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'
        associate_tag = 'httpwwwopen01 - 20'

        amazon = bottlenose.Amazon(key_access, key_secret, associate_tag, Region='US')

        # BrowseNodes,EditorialReview,Similarities,ItemAttributes
        xml_response = amazon.ItemLookup(ItemId=itemid, IdType='ISBN', SearchIndex='Books',
                                         ResponseGroup='Offers,OfferFull,SalesRank,ItemAttributes')
        # xml_response = amazon.ItemLookup(ItemId=itemid, ResponseGroup='BrowseNodes,EditorialReview,Similarities,ItemAttributes')
        root = ET.fromstring(xml_response)

        for items in root:
            if items.tag.split('}')[1] == 'Items':
                items_list = []
                for item in items:
                    if item.tag.split('}')[1] == 'Item':
                        item_des = self.__initialize_item_amazon()

                        for attr in item:
                            if attr.tag.split('}')[1] == 'ASIN':
                                item_des[attr.tag.split('}')[1]] = attr.text
                            if attr.tag.split('}')[1] == 'EditorialReviews':
                                editorialReviews = []
                                for editorialReview in attr:
                                    if editorialReview.tag.split('}')[1] == 'EditorialReview':
                                        editorialReviewAttr_d = dict()
                                        for editorialReviewAttr in editorialReview:
                                            editorialReviewAttr_d[
                                                editorialReviewAttr.tag.split('}')[1]] = editorialReviewAttr.text
                                        editorialReviews.append(editorialReviewAttr_d)
                                item_des[attr.tag.split('}')[1]] = editorialReviews

                            if attr.tag.split('}')[1] == 'SalesRank':
                                item_des[attr.tag.split('}')[1]] = attr.text

                            if attr.tag.split('}')[1] == 'OfferSummary':
                                for offer in attr:
                                    if offer.tag.split('}')[-1] == 'LowestNewPrice':
                                        item_des['LowestNewPrice'] = offer[0].text

                                    if offer.tag.split('}')[-1] == 'LowestUsedPrice':
                                        item_des['LowestUsedPrice'] = offer[0].text

                            if attr.tag.split('}')[1] == 'ItemAttributes':
                                for itemAttributes in attr:
                                    if itemAttributes.tag.split('}')[-1] == 'Binding':
                                        item_des['Binding'] = itemAttributes.text

                                    if itemAttributes.tag.split('}')[-1] == 'Publisher':
                                        item_des['Publisher'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'Title':
                                        item_des['Title'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'Author':
                                        item_des['Author'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'PublicationDate':
                                        item_des['PublicationDate'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'NumberOfPages':
                                        item_des['NumberOfPages'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'ReleaseDate':
                                        item_des['ReleaseDate'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'EISBN':
                                        item_des['EISBN'] = itemAttributes.text
                                    if itemAttributes.tag.split('}')[-1] == 'PackageDimensions':
                                        for packageDimensions in itemAttributes:
                                            if packageDimensions.tag.split('}')[-1] == 'Weight':
                                                item_des['Weight'] = packageDimensions.text
                                                break

                        items_list.append(item_des)

                return items_list

        return None

    def __initialize_item_amazon(self):
        item_des=dict()
        item_des['ASIN'] = None
        item_des['LowestUsedPrice'] = None
        item_des['LowestNewPrice'] = None
        item_des['SalesRank'] = None
        item_des['Binding'] = None
        item_des['Merchant'] = None
        item_des['Price'] = None
        item_des['Condition'] = None
        item_des['Weight'] = None
        item_des['EditorialReviews'] = None
        item_des['Publisher'] = None
        item_des['Title'] = None
        item_des['Author'] = None
        item_des['PublicationDate'] = None
        item_des['NumberOfPages'] = None
        item_des['ReleaseDate'] = None
        item_des['Digital List Price Scrape'] = None
        item_des['Print List Price Scrape'] = None
        item_des['Kindle Price Scrape'] = None
        item_des['SalesRank Scrape'] = None
        item_des['NumberOfReviews'] = None
        item_des['Rating'] = None
        item_des['EISBN'] = None
        item_des['NumberOfReviews'] = None
        item_des['Rating'] =None
        item_des['PageDescription']=None
        item_des['DescriptionScrape']=None
        item_des['EditorialReviewsScrape']=None
        return item_des
