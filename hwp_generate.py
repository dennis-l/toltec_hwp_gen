
import csv
import numpy as np

def create_data_from_avg(band_avgs):
    length = 311
    min = 10
    max = 320
    freq = np.linspace(min, max, length) 

    Tx_C  = np.zeros_like(freq) 
    Rx_C  = np.zeros_like(freq) 
    Abs_C = np.zeros_like(freq) 
    Tx_L  = np.zeros_like(freq) 
    Rx_L  = np.zeros_like(freq) 
    Abs_L = np.zeros_like(freq) 

    for band in band_avgs:
        # asserts that the sum of transmission, reflection, and absorption == 1 (or is at least somewhat close)
        assert np.allclose(1.0, (band_avgs[band]['Tx_C'] + band_avgs[band]['Rx_C'] + band_avgs[band]['Abs_C']))
        assert np.allclose(1.0, (band_avgs[band]['Tx_L'] + band_avgs[band]['Rx_L'] + band_avgs[band]['Abs_L']))
        
        Tx_C[band_avgs[band]['min_GHz'] - min: band_avgs[band]['max_GHz'] - min]   = band_avgs[band]['Tx_C']
        Rx_C[band_avgs[band]['min_GHz'] - min: band_avgs[band]['max_GHz'] - min]   = band_avgs[band]['Rx_C']
        Abs_C[band_avgs[band]['min_GHz'] - min: band_avgs[band]['max_GHz'] - min]  = band_avgs[band]['Abs_C']

        Tx_L[band_avgs[band]['min_GHz'] - min: band_avgs[band]['max_GHz'] - min]   = band_avgs[band]['Tx_L']
        Rx_L[band_avgs[band]['min_GHz'] - min: band_avgs[band]['max_GHz'] - min]   = band_avgs[band]['Rx_L']
        Abs_L[band_avgs[band]['min_GHz'] - min: band_avgs[band]['max_GHz'] - min]  = band_avgs[band]['Abs_L']

    return np.column_stack((freq,Tx_C,Rx_C,Abs_C,Tx_L,Rx_L,Abs_L))

def export_csv(write_obj, csv_name='custom_hwp_model.csv'):
    with open(csv_name, 'w') as autogenhwp:
        # write header matter
        autogenhwp.write(',Capacitive axis,,,Inductive axis,,,,,,auto-generated-hwp,,,,Temperature (K),\n')
        autogenhwp.write('Freq,Tx_C,Rx_C,Abs_C,Tx_L,Rx_L,Abs_L,DPh,45d X-Pol,Model:,autogen_toltec_hwp,,,,emitted,reflected,\n')
        
        # iterate through to write
        for idx, row in enumerate(write_obj):

            # handle some special cases
            if idx == 0:
                autogenhwp.write(str(int(row[0])) + ',' + ','.join([str(i) for i in row[1:]]) + ',251.06786,-7.0777609,,nC=X,,,,290,45,\n')
                continue
            if idx == 1:
                autogenhwp.write(str(int(row[0])) + ',' + ','.join([str(i) for i in row[1:]]) + ',247.54163,-7.1567758,,nL=X,,,,290,45,\n')
                continue

            # otherwise write rows
            autogenhwp.write(str(int(row[0])) + ',' + ','.join([str(i) for i in row[1:]]) + '244.12638,-7.2096205,,,,,,290,45,\n')

def generate_hwp_model(band_avgs):
    write_obj = create_data_from_avg(band_avgs)
    export_csv(write_obj)


if __name__ == '__main__':
   
    band_avgs = {
        'low': {
            'min_GHz': 128, 'max_GHz': 170,
            'Tx_C':  0.985658,
            'Rx_C':  0.00716651,
            'Abs_C': 0.00717574,
        
            'Tx_L':  0.932995,
            'Rx_L':  0.0152067,
            'Abs_L': 0.051798
        },
        'mid': {
            'min_GHz': 195, 'max_GHz': 244,
            'Tx_C':  0.985658,
            'Rx_C':  0.00716651,
            'Abs_C': 0.00717574,
        
            'Tx_L':  0.932995,
            'Rx_L':  0.0152067,
            'Abs_L': 0.051798
        },
        'high': {
            'min_GHz': 245, 'max_GHz': 310,
            'Tx_C':  0.985658,
            'Rx_C':  0.00716651,
            'Abs_C': 0.00717574,
        
            'Tx_L':  0.932995,
            'Rx_L':  0.0152067,
            'Abs_L': 0.051798   
        }
    }

    write_obj = create_data_from_avg(band_avgs)
    export_csv(write_obj, csv='test_generation.csv')

