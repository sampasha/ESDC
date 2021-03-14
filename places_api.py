import requests
import pandas as pd

def google_data(business_code,business_name,GMAPS_API_KEY):   
    for b_code in business_code:
        info_url = "https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input={}&inputtype=textquery&fields=place_id,photos,user_ratings_total,business_status,formatted_address,name,opening_hours,rating&key=".format(business_name+" "+str(b_code))+GMAPS_API_KEY
        response = requests.get(info_url)
        candidate = response.json()['candidates'][0]
        
        ls = ['name','status','address','rating','number','review time','review text','author url','website','photo_url']
    
        business_dict = dict((el,"Not found") for el in ls)
        business_dict['score'] = 0
        if 'name' in candidate:
            business_dict['name'] = candidate['name']
            business_dict['score'] +=1
        if 'business_status' in candidate:
            business_dict['status'] = candidate['business_status']
            business_dict['score']+=1
        if 'formatted_address' in candidate:
            business_dict['address'] = candidate['formatted_address']
            business_dict['score']+=1
        if 'rating' in candidate:
            business_dict['rating'] = str(candidate['rating'])
            business_dict['score']+=1

        if 'photos' in candidate:
            if 'photo_reference' in candidate['photos'][0]:
                business_dict['reference'] = candidate['photos'][0]['photo_reference']

                business_dict['score']+=1

            if 'place_id' in candidate: 
                place_id = candidate['place_id']
                place_url = "https://maps.googleapis.com/maps/api/place/details/json?place_id={}&fields=website,types,reviews,photos,icon,formatted_phone_number&key=".format(str(place_id))+GMAPS_API_KEY
                place_response = requests.get(place_url).json()['result']

                if 'formatted_phone_number' in place_response:
                    business_dict['number'] = place_response['formatted_phone_number']
                    business_dict['score']+=1

                if 'website' in place_response:
                    business_dict['website'] = place_response['website']
                    business_dict['score']+=1

                if 'reviews' in place_response:
                    review_list=[]
                    for review in place_response['reviews']:
                        review_list.append(review['time'])
                    index_id = review_list.index(max(review_list))
                    business_dict['review time'] = place_response['reviews'][index_id]['relative_time_description']
                    business_dict['score']+=1
                    business_dict['review text'] = place_response['reviews'][index_id]['text']
                    business_dict['score']+=1
                    business_dict['author url'] = place_response['reviews'][index_id]['author_url']
                    business_dict['score']+=1

            if 'reference' in business_dict:
                photo_url = "https://maps.googleapis.com/maps/api/place/photo?max_width=400&"
                photo_URL = photo_url+'photoreference='+business_dict['reference']+'&key='+GMAPS_API_KEY
                business_dict['photo_url'] = photo_URL
    
    return business_dict
