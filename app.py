from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
app = Flask(__name__)
CORS(app)
# Database connection (replace with your database details)
conn = sqlite3.connect('trading_journal.db')
@app.route('/trades', methods=['GET', 'POST'])
def trades():
    if request.method == 'GET':
        # Fetch all trades from the database
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM trades")
        trades = cursor.fetchall()
        return jsonify(trades)
    elif request.method == 'POST':
        # Insert new trade data into the database
        trade_data = request.get_json()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO trades VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", 
                       (trade_data['trade_id'], trade_data['currency_pair'], ...)) 
        conn.commit()
        return jsonify({'message': 'Trade added successfully'}), 201
# ... Other API routes for statistics, emotion analysis, etc.
if __name__ == '__main__':
    app.run(debug=True)
React (Component for Trade Log):

import React, { useState } from 'react';
function TradeLog() {
  const [tradeData, setTradeData] = useState({
    currencyPair: '',
    entryDate: '',
    entryTime: '',
    // ... other fields
  });
  const handleInputChange = (event) => {
    setTradeData({ ...tradeData, [event.target.name]: event.target.value });
  };
  const handleSubmit = async (event) => {
    event.preventDefault();
    // Send trade data to the API
    try {
      const response = await fetch('http://localhost:5000/trades', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(tradeData),
      });
      // Handle response (e.g., display success message)
    } catch (error) {
      // Handle error
    }
  };
  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label htmlFor="currencyPair">Currency Pair:</label>
        <input 
          type="text" 
          id="currencyPair" 
          name="currencyPair" 
          value={tradeData.currencyPair} 
          onChange={handleInputChange} 
        />
      </div>
      {/* ... other input fields for trade details */}
      <button type="submit">Add Trade</button>
    </form>
  );
}
export default TradeLog;
