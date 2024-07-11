#import pandas as pd

#def handle_uploaded_file(uploaded_file):
 #   if uploaded_file.name.endswith(".txt"):
  #      return uploaded_file.read().decode("utf-8")
   # elif uploaded_file.name.endswith(".csv"):
    #    df = pd.read_csv(uploaded_file)
     #   return df.to_string(index=False)
    #else:
     #   return None



# utils/file_handler.py

import os
import pandas as pd

def handle_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            return df
        except Exception as e:
            raise e
