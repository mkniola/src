import asyncio
import time
import textwrap
from datetime import datetime
import streamlit as st
from PIL import Image
import requests
# from components.oauth2client import OAuth2Client as aouth
#from components.employee import Employee
#from components.timer import IntervalTimer


async def update_time(section):
    section.header(datetime.now().strftime("%H:%M:%S"))
    time.sleep(1)
    await update_time(section)
        

def main():
    #locale.setlocale(locale.LC_TIME, "pl_PL.utf8")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    fullname, id = parse_query_string()
    print(fullname)
    section = prepare_layout(fullname, id)
    
    loop.run_until_complete(update_time(section))
    loop.close()

def extract_value(key, dictionary):
    if key in dictionary.keys():
        return dictionary[key][0]
    else:
        return "missing"

def parse_query_string():
    query_params = st.experimental_get_query_params()
    if query_params is None:
        return [None, None]
    name = extract_value("name", query_params)
    lastname = extract_value("lastname", query_params)
    id = extract_value("id", query_params)
    return [f'{name} {lastname}'.capitalize(), f'{id}']


def prepare_layout(full_name, id):

    ## title and fullname
    title, fullname = st.columns(2)
    with title:
        st.header('PANEL PRACOWNIKA')
        st.caption(f'{datetime.now().strftime("%A")}, {datetime.now().strftime("%d-%m-%Y")}')
    with fullname:
        st.header(full_name)
        st.caption(f'Identyfikator pracownika: {id}')
     ## logo, quote of the day
    author, lines = get_random_quote(80)
    for line in lines:
        st.text(line)
    st.caption(author)
    st.markdown('---')

    ## logo, date, time, temperature
    logo_img = Image.open('images/miminu_logo.jpg')
    logo, currenttime, temperature = st.columns(3)
    with logo:
        st.image(logo_img, width=180)
    with currenttime:
        st.subheader("Paterek")
        time_section = st.empty()
    with temperature:
        st.metric(label="Temperature", value="70 °F", delta="1.2 °F")

    st.markdown('---')
   
    ## time tracking ops
    st.subheader('RAPORTOWANIE CZASU PRACY')
    st.markdown('---')

    checkin, checkout, absence = st.columns(3)

    with checkin:
        st.button('ZAMELDUJ SIE', key='checkinBtn', help='Rozpoczecie pracy')

    with checkout:
        st.button('ODMELDUJ SIE', key='checkoutBtn', help='Zakonczenie pracy')

    with absence:
        st.button('ZGLOS NIEOBECNOSC', key='absenceBtn', help='Uprzedz, ze nie bedzie cie w pracy')

    return time_section


## function that gets the random quote
def get_random_quote(text_width):
    try:
        ## making the get request
        response = requests.get("https://quote-garden.herokuapp.com/api/v3/quotes/random", verify=False)
        if response.status_code == 200:
            ## extracting the core data
            json_data = response.json()
            data = json_data['data']
            ## getting the quote from the data
            # Wrap this text.
            wrapper = textwrap.TextWrapper(width=text_width)
            word_list = wrapper.wrap(text=data[0]['quoteText'])
            quote_author = data[0]['quoteAuthor']
            return [quote_author, word_list]
    except Exception as e:
        print("Something went wrong! Try Again!")
        print(e)
        return [None, None]
    


if __name__ == "__main__":
    main()

