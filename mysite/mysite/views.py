from django.shortcuts import render
from django.conf import settings
from mysite.models import MGNREGAData  # ✅ Import your model

# --- HELPER FUNCTIONS ---

def list_districts():
    return sorted(MGNREGAData.objects.values_list("district_name", flat=True).distinct())

def list_years():
    return sorted(MGNREGAData.objects.values_list("fin_year", flat=True).distinct(), reverse=True)


# --- INDEX VIEW ---

def index(request):
    q_district = request.GET.get("district", "").strip()
    q_year = request.GET.get("year", "").strip()

    context = {
        "districts": list_districts(),
        "years": list_years(),
        "selected_district": q_district,
        "selected_year": q_year,
        "table_rows": [],
        "error": None,
    }

    # If no district selected, just show dropdowns
    if not q_district:
        return render(request, "index.html", context)

    qs = MGNREGAData.objects.filter(district_name__icontains=q_district)

    if q_year:
        qs = qs.filter(fin_year=q_year)

    if not qs.exists():
        context["error"] = "No data found for this district/year."
        return render(request, "index.html", context)

    # Columns you were displaying earlier
    cols = [
    "fin_year", "month", "state_name", "district_name",
    "approved_labour_budget", "average_wage_rate",
    "total_households_worked", "total_expenditure", "women_persondays"
    ]


    # Prepare table rows
    table_rows = list(qs.values(*cols)[:100])
    context["table_rows"] = table_rows
    return render(request, "index.html", context)


# --- SUMMARY VIEW ---

def summary(request):
    q_district = request.GET.get("district", "").strip()
    q_year = request.GET.get("year", "").strip()

    if not q_district:
        return render(request, "summary.html", {"error": "Please select a district."})

    qs = MGNREGAData.objects.filter(district_name__icontains=q_district)

    if q_year:
        qs = qs.filter(fin_year=q_year)

    if not qs.exists():
        return render(request, "summary.html", {"error": "No data found for selection."})

    # Convert queryset to list of dicts for calculations
    df = list(qs.values())

    import pandas as pd
    df = pd.DataFrame(df)

    # --- SUMMARY METRICS ---
    summary = {
            "Records Found": len(df),
            "Total Expenditure": round(df["total_expenditure"].sum(), 2) if "total_expenditure" in df else "-",
            "Individuals Worked": int(df["total_households_worked"].sum()) if "total_households_worked" in df else "-",
            "Average Wage Rate": round(df["average_wage_rate"].mean(), 2) if "average_wage_rate" in df else "-",
            "Total Women Persondays": int(df["women_persondays"].sum()) if "women_persondays" in df else "-",
        }


    # --- CHART DATA ---
    chart1, chart2, chart3 = {}, {}, {}
    
    if "month" in df.columns and "total_expenditure" in df.columns:
        grouped = df.groupby("month")["total_expenditure"].sum().reset_index()
        chart1 = {"labels": grouped["month"].tolist(), "values": grouped["total_expenditure"].tolist()}

    if "month" in df.columns and "women_persondays" in df.columns:
        grouped2 = df.groupby("month")["women_persondays"].sum().reset_index()
        chart2 = {"labels": grouped2["month"].tolist(), "values": grouped2["women_persondays"].tolist()}

    if "month" in df.columns and "average_wage_rate" in df.columns:
        grouped3 = df.groupby("month")["average_wage_rate"].mean().reset_index()
        chart3 = {"labels": grouped3["month"].tolist(), "values": grouped3["average_wage_rate"].tolist()}


    return render(request, "summary.html", {
        "district": q_district,
        "year": q_year,
        "summary": summary,
        "chart1": chart1,
        "chart2": chart2,
        "chart3": chart3,
    })
