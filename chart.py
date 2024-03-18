import streamlit as st
import json
import altair as alt
import pandas as pd

json_response = [
    {'slotId': '1c4575db71154f7ec978b7a1', 'date': '2024-03-06T22:30:00.000Z', 'bookingPerSlot': 5, 'bookedAppointments': 0},
    {'slotId': '1c4575db71154f7ec978b7a2', 'date': '2024-03-06T22:30:00.000Z', 'bookingPerSlot': 5, 'bookedAppointments': 0},
    {'slotId': '1c4575db71154f7ec978b7a3', 'date': '2024-03-06T22:30:00.000Z', 'bookingPerSlot': 5, 'bookedAppointments': 5},
    {'slotId': '1c4575db71154f7ec978b7a4', 'date': '2024-04-06T22:30:00.000Z', 'bookingPerSlot': 5, 'bookedAppointments': 4},
    {'slotId': '1c4575db71154f7ec978b7a5', 'date': '2024-04-06T22:30:00.000Z', 'bookingPerSlot': 5, 'bookedAppointments': 3},
    {'slotId': '1c4575db71154f7ec978b7a6', 'date': '2024-05-06T22:30:00.000Z', 'bookingPerSlot': 5, 'bookedAppointments': 2},

]

df = pd.DataFrame(json_response)

chart = alt.Chart(df).mark_bar().encode(
    x='date:N',
    y='bookedAppointments:Q',
    tooltip=['bookingPerSlot','bookedAppointments', 'date']
).interactive()

st.altair_chart(chart, use_container_width=True)
