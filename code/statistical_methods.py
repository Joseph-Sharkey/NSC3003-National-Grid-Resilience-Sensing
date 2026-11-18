import torch as t 
import numpy as np 

class StatMethods:
    def outage_integral(self, month_data):
        data = t.tensor((month_data)["f"].to_numpy())
        locs = t.where(abs(data - 50) > 0.2)
        return t.sum(t.abs(data[locs])) #this isn't correct, needs an update

    def minor_outage_freq(self, month_data):
        data = t.tensor((month_data)["f"].to_numpy())
        locs = t.where(abs(data - 50) > 0.2)
        return len(data[locs])
    
    def major_outage_instances(self, month_data):
        data = t.tensor(month_data["f"].to_numpy())
        locs = t.where(abs(data-50) > 0.5)
        return data[locs]
    
    def major_outage_periods(self, month_data):
        pass 

    def recovery_rates(self, month_data):
        threshold = 49.8
        data = t.tensor(month_data["f"].to_numpy())
        deviation_locs = t.where(data < threshold)[0]
        if len(deviation_locs) == 0:
            return []
        breaks = t.where(deviation_locs[1:] - deviation_locs[:-1] > 1)[0]+1 
        starts = t.cat((deviation_locs[:1], deviation_locs[breaks]))
        ends = t.cat((deviation_locs[breaks-1], deviation_locs[-1:]))

        results = []
        for start, end in zip(starts, ends):
            segment = data[start:end+1]
            min_idx = t.argmin(segment) + start 
            min_val = data[min_idx]
            recovery_candidates = t.where(
                data[end+1:] >= threshold
            )[0]
            if len(recovery_candidates) == 0:
                continue 
            recovery_idx = end + 1 + recovery_candidates[0]
            recovery_val = data[recovery_idx]
            rate = (recovery_val - min_val) / (recovery_idx - min_idx)

            results.append({
                "minimum": min_val.item(),
                "minimum_time": min_idx.item(),
                "recovery_value": recovery_val.item(),
                "recovery_time": recovery_idx.item(),
                "recovery_rate": rate.item()
            })
        return results
            


    
    def monthly_variance(self, month_data):
        data = t.tensor(month_data["f"].to_numpy())
        return data.var().item()

    def histogram(self, month_data):
        data = month_data["f"].to_numpy()
        bins = np.linspace(48, 52, 101)
        hist, _ = np.histogram(data, bins=bins)
        return hist
    

