import xmltodict
import json
from bson import json_util
from pymongo import MongoClient
import csv
import boto
from boto.s3.key import Key
import psycopg2
from datetime import datetime
import sys, os
from xml.parsers.expat import ExpatError
import mysql.connector

import xml.etree.ElementTree as ET


class xml_parse:

    def parse_user_agent_xml_file(self, input_file_path):

        user_agent_list=[]

        tree = ET.parse(input_file_path)
        root = tree.getroot()
        for child in root:
            for child_1 in child:
                if child_1.tag=='useragent':
                    user_agent_list.append(child_1.attrib)

        print ""


x=xml_parse()
x.parse_user_agent_xml_file("useragentswitcher.xml")

