"""Sample trial data for local development when ClinicalTrials.gov is unreachable."""

MOCK_TRIALS = [
    {
        "nct_id": "NCT05112107",
        "title": "Osimertinib Plus Savolitinib in EGFRm NSCLC With MET-driven Resistance (SAVANNAH)",
        "sponsor_name": "AstraZeneca",
        "sponsor_type": "industry",
        "phase": "Phase 2",
        "status": "RECRUITING",
        "conditions": ["Non-Small Cell Lung Cancer", "NSCLC"],
        "interventions": [
            {"type": "Drug", "name": "Osimertinib", "other_names": ["Tagrisso", "AZD9291"]},
            {"type": "Drug", "name": "Savolitinib", "other_names": ["AZD6094"]},
        ],
        "countries": ["United States", "United Kingdom", "France", "Germany", "Japan"],
        "enrollment": 290,
        "enrollment_type": "Actual",
        "start_date": "2021-11-01",
        "primary_completion_date": "2026-06-30",
        "brief_summary": (
            "A Phase II, open-label study to assess the efficacy and safety of osimertinib "
            "combined with savolitinib in patients with EGFRm NSCLC whose disease has progressed "
            "on osimertinib and who have MET-driven resistance."
        ),
        "primary_outcomes": [
            {"measure": "Objective Response Rate (ORR) per RECIST 1.1 by BICR"},
        ],
        "source": "ctgov",
        "raw_json": {},
    },
    {
        "nct_id": "NCT04685070",
        "title": "Adagrasib (MRTX849) in Combination With Pembrolizumab in KRAS G12C-Mutated NSCLC",
        "sponsor_name": "Mirati Therapeutics",
        "sponsor_type": "industry",
        "phase": "Phase 2",
        "status": "RECRUITING",
        "conditions": ["Non-Small Cell Lung Cancer", "KRAS G12C Mutation"],
        "interventions": [
            {"type": "Drug", "name": "Adagrasib", "other_names": ["MRTX849", "Krazati"]},
            {"type": "Biological", "name": "Pembrolizumab", "other_names": ["Keytruda", "MK-3475"]},
        ],
        "countries": ["United States", "Canada", "Spain", "Italy"],
        "enrollment": 160,
        "enrollment_type": "Anticipated",
        "start_date": "2021-02-15",
        "primary_completion_date": "2026-09-01",
        "brief_summary": (
            "A Phase 2 study evaluating adagrasib in combination with pembrolizumab in patients "
            "with previously untreated, locally advanced or metastatic NSCLC harbouring a KRAS G12C mutation."
        ),
        "primary_outcomes": [
            {"measure": "Progression-Free Survival (PFS) per RECIST 1.1"},
        ],
        "source": "ctgov",
        "raw_json": {},
    },
    {
        "nct_id": "NCT05765526",
        "title": "Datopotamab Deruxtecan (Dato-DXd) Versus Docetaxel in Previously Treated NSCLC (TROPION-Lung08)",
        "sponsor_name": "Daiichi Sankyo",
        "sponsor_type": "industry",
        "phase": "Phase 3",
        "status": "RECRUITING",
        "conditions": ["Non-Small Cell Lung Cancer"],
        "interventions": [
            {"type": "Drug", "name": "Datopotamab deruxtecan", "other_names": ["Dato-DXd", "DS-1062"]},
            {"type": "Drug", "name": "Docetaxel", "other_names": []},
        ],
        "countries": ["United States", "Germany", "Japan", "China", "Australia"],
        "enrollment": 603,
        "enrollment_type": "Anticipated",
        "start_date": "2023-04-10",
        "primary_completion_date": "2027-03-01",
        "brief_summary": (
            "A randomised, open-label, Phase 3 study comparing datopotamab deruxtecan to docetaxel "
            "in patients with previously treated, advanced or metastatic NSCLC without actionable genomic alterations."
        ),
        "primary_outcomes": [
            {"measure": "Progression-Free Survival (PFS)"},
            {"measure": "Overall Survival (OS)"},
        ],
        "source": "ctgov",
        "raw_json": {},
    },
    {
        "nct_id": "NCT05263856",
        "title": "Lazertinib Plus Amivantamab vs Osimertinib in EGFR-Mutated Advanced NSCLC (MARIPOSA)",
        "sponsor_name": "Janssen Research & Development",
        "sponsor_type": "industry",
        "phase": "Phase 3",
        "status": "RECRUITING",
        "conditions": ["Non-Small Cell Lung Cancer", "EGFR Mutation"],
        "interventions": [
            {"type": "Biological", "name": "Amivantamab", "other_names": ["JNJ-61186372", "Rybrevant"]},
            {"type": "Drug", "name": "Lazertinib", "other_names": ["JNJ-73841937", "Leclaza"]},
            {"type": "Drug", "name": "Osimertinib", "other_names": ["Tagrisso"]},
        ],
        "countries": ["United States", "South Korea", "Japan", "Germany", "France"],
        "enrollment": 1074,
        "enrollment_type": "Anticipated",
        "start_date": "2022-03-14",
        "primary_completion_date": "2027-01-01",
        "brief_summary": (
            "Phase 3 study comparing lazertinib plus amivantamab to osimertinib as first-line "
            "treatment in patients with EGFR-mutated (exon 19 deletions or L858R) locally advanced "
            "or metastatic NSCLC."
        ),
        "primary_outcomes": [{"measure": "Progression-Free Survival (PFS) by Blinded Independent Central Review"}],
        "source": "ctgov",
        "raw_json": {},
    },
    {
        "nct_id": "NCT04736706",
        "title": "Tarlatamab (AMG 757) in Small Cell Lung Cancer After Platinum-Based Chemotherapy (DeLLphi-301)",
        "sponsor_name": "Amgen",
        "sponsor_type": "industry",
        "phase": "Phase 2",
        "status": "RECRUITING",
        "conditions": ["Small Cell Lung Cancer", "SCLC"],
        "interventions": [
            {"type": "Biological", "name": "Tarlatamab", "other_names": ["AMG 757"]},
        ],
        "countries": ["United States", "Germany", "Spain", "Italy", "Australia"],
        "enrollment": 220,
        "enrollment_type": "Actual",
        "start_date": "2021-03-08",
        "primary_completion_date": "2026-06-30",
        "brief_summary": (
            "Phase 2 study of tarlatamab, a bispecific T-cell engager targeting DLL3, in patients "
            "with small cell lung cancer who have progressed on platinum-based chemotherapy."
        ),
        "primary_outcomes": [{"measure": "Objective Response Rate (ORR) by BICR"}],
        "source": "ctgov",
        "raw_json": {},
    },
    {
        "nct_id": "NCT05361655",
        "title": "Ifinatamab Deruxtecan (I-DXd) in Relapsed/Refractory SCLC (IDeate-Lung01)",
        "sponsor_name": "Daiichi Sankyo",
        "sponsor_type": "industry",
        "phase": "Phase 2",
        "status": "RECRUITING",
        "conditions": ["Small Cell Lung Cancer"],
        "interventions": [
            {"type": "Drug", "name": "Ifinatamab deruxtecan", "other_names": ["I-DXd", "DS-7300"]},
        ],
        "countries": ["United States", "Japan", "United Kingdom", "France"],
        "enrollment": 195,
        "enrollment_type": "Anticipated",
        "start_date": "2022-06-01",
        "primary_completion_date": "2026-12-01",
        "brief_summary": (
            "An open-label, multicenter Phase 2 study evaluating the efficacy and safety of "
            "ifinatamab deruxtecan in patients with relapsed or refractory small cell lung cancer."
        ),
        "primary_outcomes": [{"measure": "Objective Response Rate (ORR)"}],
        "source": "ctgov",
        "raw_json": {},
    },
    {
        "nct_id": "NCT05456893",
        "title": "Pembrolizumab Plus Chemotherapy in Resectable NSCLC — Neoadjuvant/Adjuvant (KEYNOTE-671)",
        "sponsor_name": "Merck Sharp & Dohme",
        "sponsor_type": "industry",
        "phase": "Phase 3",
        "status": "RECRUITING",
        "conditions": ["Non-Small Cell Lung Cancer", "Resectable NSCLC"],
        "interventions": [
            {"type": "Biological", "name": "Pembrolizumab", "other_names": ["Keytruda", "MK-3475"]},
            {"type": "Drug", "name": "Cisplatin", "other_names": []},
            {"type": "Drug", "name": "Gemcitabine", "other_names": []},
        ],
        "countries": ["United States", "Canada", "Germany", "France", "Japan", "China"],
        "enrollment": 786,
        "enrollment_type": "Actual",
        "start_date": "2022-07-18",
        "primary_completion_date": "2027-09-01",
        "brief_summary": (
            "Phase 3, randomized, double-blind trial of perioperative pembrolizumab plus "
            "platinum-based chemotherapy vs placebo plus chemotherapy in patients with resectable "
            "Stage II–IIIB NSCLC."
        ),
        "primary_outcomes": [
            {"measure": "Event-Free Survival (EFS)"},
            {"measure": "Overall Survival (OS)"},
        ],
        "source": "ctgov",
        "raw_json": {},
    },
    {
        "nct_id": "NCT04409574",
        "title": "Patritumab Deruxtecan (HER3-DXd) in EGFR-Mutated NSCLC After EGFR TKI and Platinum Chemotherapy (HERTHENA-Lung01)",
        "sponsor_name": "Daiichi Sankyo",
        "sponsor_type": "industry",
        "phase": "Phase 2",
        "status": "RECRUITING",
        "conditions": ["Non-Small Cell Lung Cancer", "HER3", "EGFR Mutation"],
        "interventions": [
            {"type": "Drug", "name": "Patritumab deruxtecan", "other_names": ["HER3-DXd", "U3-1402"]},
        ],
        "countries": ["United States", "Japan", "South Korea", "Taiwan", "Germany"],
        "enrollment": 225,
        "enrollment_type": "Actual",
        "start_date": "2020-09-24",
        "primary_completion_date": "2026-03-31",
        "brief_summary": (
            "A global Phase 2 study of patritumab deruxtecan in patients with EGFR-mutated NSCLC "
            "who have previously received an EGFR TKI and platinum-based chemotherapy."
        ),
        "primary_outcomes": [{"measure": "Objective Response Rate (ORR) by BICR per RECIST 1.1"}],
        "source": "ctgov",
        "raw_json": {},
    },
    {
        "nct_id": "NCT05091567",
        "title": "Glecirasib (JAB-21822) in KRAS G12C-Mutated Solid Tumors Including NSCLC",
        "sponsor_name": "Jacobio Pharmaceuticals",
        "sponsor_type": "industry",
        "phase": "Phase 1",
        "status": "RECRUITING",
        "conditions": ["Non-Small Cell Lung Cancer", "Colorectal Cancer", "KRAS G12C"],
        "interventions": [
            {"type": "Drug", "name": "Glecirasib", "other_names": ["JAB-21822"]},
        ],
        "countries": ["United States", "China", "Australia"],
        "enrollment": 180,
        "enrollment_type": "Anticipated",
        "start_date": "2021-11-15",
        "primary_completion_date": "2026-08-01",
        "brief_summary": (
            "First-in-human Phase 1/2 study evaluating the safety, tolerability, PK, and "
            "preliminary antitumour activity of glecirasib in patients with KRAS G12C-mutated "
            "advanced solid tumours."
        ),
        "primary_outcomes": [{"measure": "Dose-Limiting Toxicities (DLT)"}],
        "source": "ctgov",
        "raw_json": {},
    },
    {
        "nct_id": "NCT04512846",
        "title": "Amivantamab Plus Carboplatin-Pemetrexed vs Carboplatin-Pemetrexed in EGFR Exon 20 Insertion NSCLC (PAPILLON)",
        "sponsor_name": "Janssen Research & Development",
        "sponsor_type": "industry",
        "phase": "Phase 3",
        "status": "ACTIVE_NOT_RECRUITING",
        "conditions": ["Non-Small Cell Lung Cancer", "EGFR Exon 20 Insertion"],
        "interventions": [
            {"type": "Biological", "name": "Amivantamab", "other_names": ["JNJ-61186372", "Rybrevant"]},
            {"type": "Drug", "name": "Carboplatin", "other_names": []},
            {"type": "Drug", "name": "Pemetrexed", "other_names": ["Alimta"]},
        ],
        "countries": ["United States", "Netherlands", "South Korea", "China", "Taiwan"],
        "enrollment": 308,
        "enrollment_type": "Actual",
        "start_date": "2020-12-07",
        "primary_completion_date": "2025-12-31",
        "brief_summary": (
            "Phase 3 study of amivantamab plus chemotherapy vs chemotherapy alone in patients "
            "with advanced NSCLC with EGFR exon 20 insertion mutations, who have not received prior systemic therapy."
        ),
        "primary_outcomes": [
            {"measure": "Progression-Free Survival (PFS) by Blinded Independent Central Review"},
        ],
        "source": "ctgov",
        "raw_json": {},
    },
    {
        "nct_id": "NCT04925427",
        "title": "Neoadjuvant Nivolumab Plus Chemotherapy vs Chemotherapy in Resectable NSCLC (CheckMate 816)",
        "sponsor_name": "Bristol-Myers Squibb",
        "sponsor_type": "industry",
        "phase": "Phase 3",
        "status": "COMPLETED",
        "conditions": ["Non-Small Cell Lung Cancer", "Resectable NSCLC"],
        "interventions": [
            {"type": "Biological", "name": "Nivolumab", "other_names": ["Opdivo", "BMS-936558"]},
            {"type": "Drug", "name": "Cisplatin", "other_names": []},
            {"type": "Drug", "name": "Paclitaxel", "other_names": ["Taxol"]},
        ],
        "countries": ["United States", "Canada", "Germany", "France", "Italy", "Spain"],
        "enrollment": 358,
        "enrollment_type": "Actual",
        "start_date": "2017-07-19",
        "primary_completion_date": "2024-03-01",
        "brief_summary": (
            "A Phase 3, randomized, open-label trial of neoadjuvant nivolumab combined with "
            "platinum-based chemotherapy versus platinum-based chemotherapy in patients with "
            "resectable Stage IB-IIIA NSCLC."
        ),
        "primary_outcomes": [
            {"measure": "Pathological Complete Response (pCR)"},
            {"measure": "Event-Free Survival (EFS)"},
        ],
        "source": "ctgov",
        "raw_json": {},
    },
    {
        "nct_id": "NCT03976362",
        "title": "Sotorasib (AMG 510) vs Docetaxel in KRAS p.G12C Mutated Advanced NSCLC (CodeBreaK 200)",
        "sponsor_name": "Amgen",
        "sponsor_type": "industry",
        "phase": "Phase 3",
        "status": "COMPLETED",
        "conditions": ["Non-Small Cell Lung Cancer", "KRAS G12C"],
        "interventions": [
            {"type": "Drug", "name": "Sotorasib", "other_names": ["AMG 510", "Lumakras"]},
            {"type": "Drug", "name": "Docetaxel", "other_names": []},
        ],
        "countries": ["United States", "Germany", "France", "Japan", "Australia"],
        "enrollment": 345,
        "enrollment_type": "Actual",
        "start_date": "2019-11-18",
        "primary_completion_date": "2023-06-30",
        "brief_summary": (
            "A global Phase 3 randomised controlled trial of sotorasib (AMG 510) versus docetaxel "
            "in patients with KRAS p.G12C-mutated advanced NSCLC who have received prior platinum-based "
            "chemotherapy and anti-PD-1/L1 therapy."
        ),
        "primary_outcomes": [
            {"measure": "Progression-Free Survival (PFS) per RECIST 1.1 by BICR"},
        ],
        "source": "ctgov",
        "raw_json": {},
    },
]


def filter_mock_trials(
    query: str | None,
    phases: list[str] | None,
    status: str | None,
) -> list[dict]:
    results = MOCK_TRIALS[:]

    if query:
        q = query.lower()
        results = [
            t for t in results
            if q in t["title"].lower()
            or any(q in c.lower() for c in t["conditions"])
        ]

    if phases:
        phase_labels = {
            "1": "Phase 1", "2": "Phase 2", "3": "Phase 3",
            "4": "Phase 4", "early1": "Early Phase 1",
        }
        wanted = {phase_labels[p] for p in phases if p in phase_labels}
        if wanted:
            results = [t for t in results if t.get("phase") in wanted]

    if status and status != "all":
        status_map = {
            "recruiting": "RECRUITING",
            "active": "ACTIVE_NOT_RECRUITING",
            "completed": "COMPLETED",
        }
        ct_status = status_map.get(status)
        if ct_status:
            results = [t for t in results if t.get("status") == ct_status]

    return results
