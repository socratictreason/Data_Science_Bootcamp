import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

st.title('Get fucked you dingbat')

df = pd.DataFrame(np.random.randn(25, 3) * 10, columns=['a', 'b', 'c'])

plt.plot(df)
st.pyplot()
