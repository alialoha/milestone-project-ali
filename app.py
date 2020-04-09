from flask import Flask, render_template, request, redirect

app = Flask(__name__)

def data_fetcher():
  from alpha_vantage.timeseries import TimeSeries
  from alpha_vantage.techindicators import TechIndicators
  from matplotlib.pyplot import figure
  import matplotlib.pyplot as plt

  # Your key here
  key = 'USO50V272CD6QVE5'
  # Chose your output format, or default to JSON (python dict)
  ts = TimeSeries(key, output_format='pandas')
  ti = TechIndicators(key)

  # Get the data, returns a tuple
  # aapl_data is a pandas dataframe, aapl_meta_data is a dict
  aapl_data, aapl_meta_data = ts.get_daily(symbol='AAPL')
  # aapl_sma is a dict, aapl_meta_sma also a dict
  aapl_sma, aapl_meta_sma = ti.get_sma(symbol='AAPL')
  
  return aapl_data

  # Visualization
  # figure(num=None, figsize=(15, 6), dpi=80, facecolor='w', edgecolor='k')
  # aapl_data['4. close'].plot()
  # plt.tight_layout()
  # plt.grid()
  # plt.show()

def data_plotter(Data):
  from bokeh.plotting import figure, output_file, show, save
  # prepare some data
  x = Data.index
  y = Data[Data.columns[3]]

# output to static HTML file
  #output_file("./templates/close_lines.html", title='closing price')

  # create a new plot
  p = figure(
    tools="pan,box_zoom,reset,save",
    x_axis_type='datetime',
    # y_axis_type="log", y_range=[0.001, 10**11], 
    title = "AAP Closing Price for last Monthes",
    x_axis_label='Date', y_axis_label='Closing price'
  )

  # add some renderers
  p.line(x, y, line_width=3)
 
  # show the results
  #show(p)
  save(p,"./templates/close_lines.html", title='closing price')

@app.route('/index')



def index():
  Data_to_plot = data_fetcher()
  data_plotter(Data_to_plot) 
  
  return render_template('close_lines.html') #plt.show() 

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(debug=True) #port=33507,
