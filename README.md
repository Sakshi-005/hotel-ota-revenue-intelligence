
# Hotel & OTA Revenue Intelligence

## About the Project

I worked on this project to understand hotel booking patterns, estimated room revenue, cancellations, and the role of different booking channels.

I used Python and Pandas for data analysis in Jupyter Notebook, then built a Streamlit dashboard to make the findings easier to explore. The main aim was to go beyond charts and identify patterns that could help hotel management make better decisions.

## Business Questions

- Which hotel type contributes more to estimated room revenue?
- How do cancellation rates differ between City Hotels and Resort Hotels?
- Which distribution channels contribute the most revenue?
- Do guests stay longer at Resort Hotels or City Hotels?
- How does estimated room revenue change over time?
- What actions could hotels consider based on these patterns?

## Key Findings

### 1. City Hotels contributed more estimated room revenue

City Hotels accounted for approximately **55.4%** of estimated room revenue, compared with 44.6% for Resort Hotels.

**Business implication:** City Hotels contributed a larger share of estimated revenue during the period studied. Management should monitor room demand and completed bookings while looking for opportunities to increase value per stay.

### 2. Resort Hotels had higher estimated revenue per completed booking

Average estimated room revenue per completed booking was approximately 400.92 for Resort Hotels and 311.38 for City Hotels. Resort Hotel stays were also longer on average.

**Business implication:** Resort Hotels could test extended-stay offers, while City Hotels could explore packages for shorter stays. Results should be evaluated against costs and demand.

### 3. Travel Agents and Tour Operators were an important channel

Travel Agents and Tour Operators (TA/TO) contributed approximately **80% of estimated room revenue** in the distribution-channel analysis.

**Business implication:** Hotels should compare channel revenue with commissions, cancellations, and customer acquisition costs. Direct-booking campaigns could be tested to see whether they improve profitability.

### 4. City Hotels had a higher cancellation rate

The analysis reported cancellation rates of approximately 40.6% for City Hotels and 27.0% for Resort Hotels.

**Business implication:** Management could investigate cancellations by lead time, booking channel, deposit type, and customer segment before changing cancellation policies.

### 5. Resort Hotel guests stayed longer

The average stay was approximately 4.32 nights at Resort Hotels, compared with 2.98 nights at City Hotels.

**Business implication:** Resort Hotels could test longer-stay packages, while City Hotels could focus on short-stay offers suited to their customers.

### 6. August 2017 was the highest-revenue month

August 2017 had approximately 1.97 million in estimated room revenue, the highest monthly figure identified in the analysis.

**Business implication:** Monthly revenue trends can support demand planning and marketing decisions. More years of data would be needed to confirm recurring seasonal patterns.

## Recommendations

Based on these findings, I would investigate the following opportunities:

- **Reduce avoidable cancellations:** Identify the booking characteristics associated with higher cancellation rates.
- **Review channel performance:** Compare revenue with commissions and acquisition costs, rather than revenue alone.
- **Test targeted offers:** Explore extended-stay offers for resorts and short-stay packages for city properties.
- **Improve demand planning:** Use monthly trends to support staffing and marketing decisions.
- **Measure profitability:** Combine booking data with operating costs and channel expenses to understand which bookings create the most value.

These are opportunities to investigate, not guaranteed outcomes. The analysis identifies patterns but does not establish causation.

## Dashboard

The interactive dashboard lets users filter by hotel type and arrival-date range.

It includes:
- Estimated room revenue
- Completed bookings
- Room nights
- Average ADR
- Monthly revenue trends
- Revenue by hotel type
- Booking status breakdown
- Revenue by distribution channel
- Booking lead-time distribution


## 🚀 Live Dashboard

Explore the interactive Hotel & OTA Revenue Intelligence dashboard:

[**View Live Dashboard**](https://hotel-ota-revenue-intelligence-mhg97pyxs5uafxwhevfvaq.streamlit.app/)


## Tools Used

- Python
- Pandas
- Plotly
- Jupyter Notebook
- Streamlit

## Revenue Calculation and Limitations

Estimated room revenue is calculated for completed stays using ADR and total nights. It is an estimate based on the available data, not audited accounting revenue or profit. The currency unit should be confirmed from the original dataset documentation.

Booking-status and cancellation analyses may include reservations that were not completed, while the revenue calculation focuses on completed stays.

The dataset covers July 2015 to August 2017, so the findings may not represent current market conditions. Operating costs and channel commissions are not included in the revenue estimates.

## How to Run the Dashboard

1. Download or clone the repository.
2. Install the required packages using `pip install -r requirements.txt`.
3. Obtain the dataset from an authorized source and configure the file path expected by `app.py`.
4. Run `streamlit run app.py`.


## What I Learned

This project gave me practical experience in preparing data, calculating business metrics, exploring booking patterns, and presenting findings through an interactive dashboard. It also helped me connect data analysis with business questions and practical recommendations.
