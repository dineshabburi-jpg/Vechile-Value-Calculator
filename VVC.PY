import datetime

class VehicleAppraisalSystem:
    def __init__(self):
        self.current_year = datetime.datetime.now().year
        # Current scrap metal market rate (approx ₹38 - ₹45 per kg)
        self.scrap_rate_per_kg = 42.0 

    def _calculate_scrap_value(self, weight_kg):
        """Internal logic for scrap metal valuation."""
        return weight_kg * self.scrap_rate_per_kg

    def evaluate_vehicle(self, data):
        # 1. Age Calculation
        age = self.current_year - data['year']
        age = max(0, age)

        # 2. Market Resale Calculation (Compounding Depreciation)
        # Using a 12% annual depreciation curve
        market_value = data['on_road_price'] * (0.88 ** age)

        # 3. Ownership History Penalty (7% drop per subsequent owner)
        owner_multiplier = 1.0 - (data['owners'] - 1) * 0.07
        market_value *= max(0.70, owner_multiplier) # Floor at 70% for ownership

        # 4. Usage/Odometer Adjustment (Standard is 12,000km/year)
        expected_km = age * 12000
        if data['odometer'] > expected_km:
            excess_km = data['odometer'] - expected_km
            usage_penalty = (excess_km / 100000) * 0.10
            market_value *= (1 - usage_penalty)

        # 5. Condition Multipliers
        condition_factors = {
            "excellent": 1.0,
            "good": 0.90,
            "fair": 0.75,
            "poor": 0.40
        }
        condition_key = data['condition'].lower()
        market_value *= condition_factors.get(condition_key, 0.70)

        # 6. Scrap Intelligence Trigger
        # Triggers if age > 15 OR condition is Poor
        scrap_value = self._calculate_scrap_value(data['weight'])
        
        is_scrap_candidate = age >= 15 or condition_key == "poor"
        
        # In professional appraisal, we offer the higher of the two 
        # but flag it if it's primarily a scrap asset.
        final_value = max(market_value, scrap_value)
        
        return {
            "resale_value": round(market_value, -2),
            "scrap_value": round(scrap_value, -2),
            "final_valuation": round(final_value, -2),
            "is_scrap_basis": is_scrap_candidate,
            "age": age
        }

    def generate_report(self, data, result):
        border = "═" * 55
        line = "─" * 55
        
        print(f"\n{border}")
        print(f"{'CERTIFIED VEHICLE VALUATION REPORT':^55}")
        print(border)
        
        # Vehicle Details
        print(f" ASSET:           {data['name'].upper()} {data['model'].upper()}")
        print(f" VINTAGE:         {data['year']} ({result['age']} Years Old)")
        print(f" USAGE:           {data['odometer']:,} KM")
        print(f" OWNERSHIP:       {data['owners']} Owner(s)")
        print(f" CONDITION:       {data['condition'].upper()}")
        print(line)
        
        # Financial Breakdown
        print(f" ORIGINAL COST:   ₹{data['on_road_price']:,.2f}")
        print(f" RESALE ESTIMATE: ₹{result['resale_value']:,.2f}")
        print(f" SCRAP ESTIMATE:  ₹{result['scrap_value']:,.2f}")
        print(line)
        
        # Scrap Intelligence Logic
        if result['is_scrap_basis']:
            print(" [!] ANALYSIS: This vehicle is a candidate for Scrappage.")
            print("     Reason: Age exceeds 15 years or Poor physical state.")
        
        print(f" FINAL VALUATION: ₹{result['final_valuation']:,.2f}")
        print(line)
        print(f" Generated on: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(border + "\n")

def main():
    appraiser = VehicleAppraisalSystem()
    
    print("WELCOME TO PRO-VALUER | Advanced Automotive Valuation Engine")
    print("Please enter vehicle details below:")
    
    try:
        user_data = {
            "name": input("Brand(eg:Tata): "),
            "model": input("Model(eg:Safari): "),
            "year": int(input("Manufacturing Year(eg:2012): ")),
            "Fuel Type": input("Fuel Type(eg:Petrol): "),
            "on_road_price": float(input("On-Road Price (INR): ")),
            "condition": input("Condition (Excellent/Good/Fair/Poor): "),
            "odometer": int(input("Odometer (KM): ")),
            "owners": int(input("Number of Previous Owners: ")),
            "weight": float(input("Vehicle Weight (KG)]: ") or 1200)
        }

        results = appraiser.evaluate_vehicle(user_data)
        appraiser.generate_report(user_data, results)

    except ValueError:
        print("\n[Error] Invalid data format. Please use numbers for Year, Price, and Odometer.")

if __name__ == "__main__":
    main()