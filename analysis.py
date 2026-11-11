import pandas as pd

# Load data
df = pd.read_csv("orders.csv")
df['status_clean'] = df['status'].str.lower().str.strip()
df['payment_type_clean'] = df['payment_type'].str.lower().str.strip().replace('cash on delivery', 'cod')

# Remove duplicates
df = df.drop_duplicates(subset=['order_id'])

# Timezone conversion
df['created_at_dt'] = pd.to_datetime(df['created_at'])
df['created_at_ist'] = df['created_at_dt'].dt.tz_convert('Asia/Kolkata') if df['created_at_dt'].dt.tz is not None else df['created_at_dt'].dt.tz_localize('UTC').dt.tz_convert('Asia/Kolkata')

# COD Final Outcomes (Delivered or RTO)
cod_final = df[(df['payment_type_clean'] == 'cod') & (df['status_clean'].isin(['delivered', 'rto']))].copy()
cod_final['week'] = cod_final['created_at_ist'].dt.to_period('W-SUN').dt.start_time.dt.date

# 1. Weekly COD Return Rate
weekly = cod_final.groupby('week')['status_clean'].value_counts().unstack(fill_value=0)
weekly['return_rate_%'] = (weekly['rto'] / (weekly['rto'] + weekly['delivered'])) * 100
print("--- Weekly COD Return Rate ---")
print(weekly[['return_rate_%']])

# 2. Top 3 Stores with highest COD Return Rate (>200 orders)
merchants = cod_final.groupby('merchant_id')['status_clean'].value_counts().unstack(fill_value=0)
merchants['total'] = merchants.get('rto', 0) + merchants.get('delivered', 0)
merchants = merchants[merchants['total'] >= 200]
merchants = merchants[~merchants.index.str.contains('TEST', case=False)] # Filter out test merchants
merchants['return_rate_%'] = (merchants['rto'] / merchants['total']) * 100
print("\n--- Top 3 Stores by Return Rate ---")
print(merchants.sort_values(by='return_rate_%', ascending=False).head(3)['return_rate_%'])
