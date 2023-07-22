import argparse
import csv
import json
import logging

import requests

# Setting up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_friends(token, user_id):
    # Function for getting a list of user's friends from VK API
    url = f'https://api.vk.com/method/friends.get'
    params = {
        'access_token': token,
        'user_id': user_id,
        'order': 'name',
        'fields': 'first_name, last_name, country, city, bdate, sex',
        'v': '5.131'
    }

    response = requests.get(url, params=params)
    data = response.json()

    def order_list_of_dicts(list_of_dicts, order_keys):
        # Auxiliary function for processing data about friends and sorting by name
        sex_mapping = {1: "женщина", 2: "мужчина"}
        ordered_list = []
        for data_dict in list_of_dicts:
            data_dict["bdate"] = data_dict["bdate"].replace(".", "-") if "bdate" in data_dict else None
            data_dict["city"] = data_dict.get("city", {}).get("title") if "city" in data_dict else None # Take only the necessary information
            data_dict["country"] = data_dict.get("country", {}).get("title") if "country" in data_dict else None 
            data_dict["sex"] = sex_mapping.get(data_dict.get("sex"), "неизвестно") if "sex" in data_dict else None  
            # Vk transmits the gender values as 1 and 2, so you need to replace

            ordered_dict = {key: data_dict[key] for key in order_keys if key in data_dict}
            ordered_list.append(ordered_dict)
        return ordered_list

    order_keys = ["first_name", "last_name", "country", "city", "bdate", "sex"] # to leave only the necessary information

    ordered_list_of_dicts = order_list_of_dicts(data['response']['items'], order_keys)
    friends_list = [json.dumps(ordered_dict, ensure_ascii=False, indent=2) for ordered_dict in ordered_list_of_dicts]

    if 'error' in data:
        error_msg = data['error']['error_msg']
        logger.error(f"Error while getting friends: {error_msg}")
        raise Exception(f"Error while getting friends: {error_msg}")

    return friends_list


def write_friends_to_file(friends_list_data, output_format, output_file):
    # Function for recording data about friends in files of different formats

    # Преобразовываем строки в словари
    data_dicts = [json.loads(data_str) for data_str in friends_list_data]

    # What parameters will be in the file
    parameters = ['First Name', 'Last Name', 'Country', 'City', 'Birth Date', 'Sex']

    try:
        if output_format == 'csv':
            # Writing data to CSV format
            with open(f'{output_file}.csv', 'w+', newline='', encoding='utf-8-sig') as output_file:
                csv_writer = csv.writer(output_file)
                csv_writer.writerow(parameters)
                for data_dict in data_dicts:
                    csv_writer.writerow([
                        data_dict.get('first_name'),
                        data_dict.get('last_name'),
                        data_dict.get('country'),
                        data_dict.get('city'),
                        data_dict.get('bdate'),
                        data_dict.get('sex')
                    ])
        if output_format == 'tsv':
            # Write data to TSV format
            with open(f'{output_file}.tsv', 'w+', newline='', encoding='utf-8-sig') as output_file:
                tsv_writer = csv.writer(output_file, delimiter='\t')
                tsv_writer.writerow(parameters)
                for data_dict in data_dicts:
                    tsv_writer.writerow([
                        data_dict.get('first_name'),
                        data_dict.get('last_name'),
                        data_dict.get('country'),
                        data_dict.get('city'),
                        data_dict.get('bdate'),
                        data_dict.get('sex')
                    ])

        if output_format == 'json':
            data_dicts = [json.loads(data_str) for data_str in friends_list_data]
            # Write data to JSON format
            with open(f'{output_file}.json', 'w', encoding='utf-8-sig') as output_file:
                json.dump(data_dicts, output_file, ensure_ascii=False, indent=4)

        logger.info(f"Report successfully generated in {output_format} format: {output_file}.{output_format.lower()}")

    except Exception as e:
        logger.error(f"An error occurred while generating the report: {str(e)}")
        raise


def read_token_from_file(file_path):
    # Function for reading a token from a file
    with open(file_path, "r", encoding="utf-8") as file:
        token = file.read().strip()
    return token


def main():
    parser = argparse.ArgumentParser(description="Creating a report about friends from VKontakte.")
    parser.add_argument("token_file", help="VK API Authorization Token")
    parser.add_argument("user_id", help="ID of the VK user for whom we are generating the report")
    parser.add_argument("--format", choices=["csv", "tsv", "json"], default="csv",
                        help="Output file format (CSV by default)")
    parser.add_argument("--output", default="report", help="The path to the output file (default is report)")

    args = parser.parse_args()
    token = read_token_from_file(args.token_file)
    friends_list_data = get_friends(token, args.user_id)
    try:

        if not friends_list_data:
            logger.warning("User has no friends or data received incorrectly.")
            print("The user has no friends or the data received is incorrect..")
            return

        # Сортируем данные по имени перед записью в файл
        friends_list_data_sorted = sorted(friends_list_data, key=lambda x: json.loads(x).get("first_name", "").lower())
        write_friends_to_file(friends_list_data_sorted, args.format, args.output)
        print(f'Report successfully generated in {args.format} format. Check {args.output}.{args.format.lower()}')


    except Exception as e:
        logger.exception(f"An error occurred: {str(e)}")
        print(f'An error occurred while generating the report. Please check the log for details: {str(e)}')


if __name__ == "__main__":
    main()

