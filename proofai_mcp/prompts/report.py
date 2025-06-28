"""Prompt for generating comprehensive unicorn startup reports."""


async def unicorn_report() -> list[dict]:
    """Generate a comprehensive unicorn startup report worth $10M+.

    This prompt guides the creation of detailed, investor-ready startup reports
    following a structured JSON format covering all aspects of a unicorn startup.
    """
    return [
        {
            "role": "system",
            "content": (
                "You are an expert startup analyst and investment advisor with 15+ years of experience "
                "evaluating unicorn startups. You have deep knowledge of market analysis, business models, "
                "competitive landscapes, and what makes startups worth $10M+. You specialize in creating "
                "comprehensive, data-driven reports that investors use to make multi-million dollar decisions.\n\n"
                
                "Your expertise includes:\n"
                "- Market sizing and opportunity analysis (TAM, SAM, SOM)\n"
                "- Competitive intelligence and positioning\n"
                "- Business model validation and unit economics\n"
                "- Go-to-market strategy optimization\n"
                "- Financial modeling and projections\n"
                "- Risk assessment and mitigation strategies\n"
                "- Team evaluation and hiring roadmaps\n"
                "- Technology assessment and IP evaluation\n\n"
                
                "You always provide specific, quantifiable data points, realistic timelines, "
                "and actionable insights backed by market research and industry benchmarks."
            ),
        },
        {
            "role": "user",
            "content": (
                "Generate a comprehensive unicorn startup report for a company with $10M+ potential. "
                "The report must be detailed, realistic, and investor-ready. Follow this exact JSON structure:\n\n"
                
                "{\n"
                '  "startup_name": "[Creative, memorable name reflecting the core value]",\n'
                '  "executive_summary": "[3-4 sentences: What the company does, market size, traction, and funding ask]",\n'
                '  "problem": {\n'
                '    "description": "[Clear problem statement affecting millions of people/businesses]",\n'
                '    "evidence": "[Statistics, studies, or data proving the problem exists and is growing]",\n'
                '    "why_now": "[Market timing, technological enablers, or regulatory changes making this the right moment]"\n'
                '  },\n'
                '  "solution": {\n'
                '    "product_description": "[Detailed explanation of the product/service and how it works]",\n'
                '    "core_innovation": "[The breakthrough technology, process, or approach that makes this unique]",\n'
                '    "competitive_edge": "[What makes this 10x better than existing solutions]",\n'
                '    "minimum_lovable_product": "[MVP that customers will love, not just tolerate]"\n'
                '  },\n'
                '  "market_opportunity": {\n'
                '    "tam": "[Total Addressable Market in $ billions with methodology]",\n'
                '    "sam": "[Serviceable Addressable Market in $ billions]",\n'
                '    "som": "[Serviceable Obtainable Market - realistic 5-year capture]",\n'
                '    "cagr": "[Compound Annual Growth Rate % with timeframe]",\n'
                '    "sources": ["[Credible market research sources like Gartner, McKinsey, etc.]"]\n'
                '  },\n'
                '  "target_customers": [\n'
                '    {\n'
                '      "persona_name": "[Specific customer persona name]",\n'
                '      "segment_type": "early_adopter",\n'
                '      "demographics": "[Age, income, location, company size, etc.]",\n'
                '      "psychographics": "[Values, motivations, behaviors, technology adoption]",\n'
                '      "pain_points": "[Specific frustrations and challenges they face daily]",\n'
                '      "buying_triggers": "[What events or situations drive them to purchase]"\n'
                '    }\n'
                '  ],\n'
                '  "unique_value_proposition": {\n'
                '    "tagline": "[Memorable 5-7 word tagline]",\n'
                '    "value_drivers": ["[3-5 specific benefits customers get]"],\n'
                '    "aha_moment": "[The moment users realize the product\'s value]"\n'
                '  },\n'
                '  "competitive_landscape": {\n'
                '    "direct_competitors": ["[Companies doing exactly the same thing]"],\n'
                '    "indirect_competitors": ["[Companies solving the problem differently]"],\n'
                '    "substitutes": ["[Alternative solutions customers use today]"],\n'
                '    "positioning_matrix": {\n'
                '      "x_axis": "[Differentiation factor like Innovation, Price, etc.]",\n'
                '      "y_axis": "[Another key factor like Quality, Speed, etc.]",\n'
                '      "quadrants": ["[How you and competitors position in each quadrant]"]\n'
                '    }\n'
                '  },\n'
                '  "business_model": {\n'
                '    "revenue_streams": ["[Multiple ways the company makes money]"],\n'
                '    "pricing_strategy": "[Detailed pricing model with rationale]",\n'
                '    "unit_economics": {\n'
                '      "ltv": "[Lifetime Value per customer with calculation method]",\n'
                '      "cac": "[Customer Acquisition Cost with breakdown]",\n'
                '      "gross_margin": "[% gross margin with industry comparison]"\n'
                '    }\n'
                '  },\n'
                '  "go_to_market_strategy": {\n'
                '    "acquisition_channels": ["[Specific channels with expected CAC and conversion rates]"],\n'
                '    "distribution_moat": "[Network effects, partnerships, or platform advantages]",\n'
                '    "sales_strategy": "[Inside sales, field sales, self-serve, etc. with rationale]",\n'
                '    "first_1000_users_plan": "[Specific tactical plan to acquire initial customers]",\n'
                '    "internationalisation_plan": "[Geographic expansion strategy and timeline]"\n'
                '  },\n'
                '  "traction_and_validation": {\n'
                '    "metrics": {\n'
                '      "waitlist_signups": "[Current numbers showing demand]",\n'
                '      "active_users": "[If launched, current user base and engagement]",\n'
                '      "revenue": "[Current revenue run rate or early sales]",\n'
                '      "growth_rate": "[Month-over-month or quarter-over-quarter growth]"\n'
                '    },\n'
                '    "proof_points": ["[Pilot programs, LOIs, awards, press coverage]"],\n'
                '    "partnerships": ["[Strategic partnerships that validate the opportunity]"]\n'
                '  },\n'
                '  "technology_and_product": {\n'
                '    "tech_stack": ["[Key technologies, frameworks, and platforms used]"],\n'
                '    "ip_or_defensibility": "[Patents, trade secrets, data moats, network effects]",\n'
                '    "product_roadmap": [\n'
                '      {\n'
                '        "milestone": "[Specific product milestone]",\n'
                '        "timeline": "[Realistic timeline for completion]"\n'
                '      }\n'
                '    ]\n'
                '  },\n'
                '  "team": {\n'
                '    "founders": [\n'
                '      {\n'
                '        "name": "[Founder name]",\n'
                '        "role": "[CEO, CTO, etc.]",\n'
                '        "background": "[Relevant experience and achievements]",\n'
                '        "linkedin": "[LinkedIn profile URL format]"\n'
                '      }\n'
                '    ],\n'
                '    "key_hires_needed": ["[Critical roles to fill with timeline and compensation]"],\n'
                '    "advisors": ["[Industry experts, successful entrepreneurs, or investors]"]\n'
                '  },\n'
                '  "vision_and_impact": {\n'
                '    "long_term_vision": "[10-20 year vision for company and industry impact]",\n'
                '    "industry_transformation": "[How this company will change the industry]",\n'
                '    "moonshot_potential": "[The biggest possible outcome and impact]"\n'
                '  },\n'
                '  "risks_and_mitigations": [\n'
                '    {\n'
                '      "risk": "[Specific business, market, or execution risk]",\n'
                '      "mitigation": "[Concrete steps to address or minimize the risk]"\n'
                '    }\n'
                '  ],\n'
                '  "financial_projections": {\n'
                '    "yearly_forecast": [\n'
                '      {\n'
                '        "year": "[Year 1, 2, 3, 4, 5]",\n'
                '        "revenue": "[$ amount with growth assumptions]",\n'
                '        "expenses": "[$ amount broken down by category]",\n'
                '        "burn_rate": "[Monthly cash burn]",\n'
                '        "profit": "[Net profit/loss with path to profitability]"\n'
                '      }\n'
                '    ],\n'
                '    "key_assumptions": ["[Critical assumptions underlying the financial model]"]\n'
                '  },\n'
                '  "funding_strategy": {\n'
                '    "current_round": "[Seed, Series A, B, etc.]",\n'
                '    "amount_raising": "[$ amount with range]",\n'
                '    "valuation_target": "[Pre/post money valuation with justification]",\n'
                '    "use_of_funds": ["[Specific allocation percentages for team, product, marketing, etc.]"],\n'
                '    "funding_milestones": ["[Key milestones to achieve before next round]"],\n'
                '    "exit_scenarios": ["[IPO timeline, acquisition targets, or strategic exits]"]\n'
                '  },\n'
                '  "metrics_to_track": {\n'
                '    "north_star_metric": "[Single most important metric for success]",\n'
                '    "core_metrics": [\n'
                '      "[Industry-specific metrics beyond the defaults]"\n'
                '    ]\n'
                '  },\n'
                '  "addendums": {\n'
                '    "pitch_deck_link": "[URL to investor pitch deck]",\n'
                '    "product_demo_link": "[URL to product demo or video]",\n'
                '    "investor_memo": "[Key points for investor conversations]",\n'
                '    "hiring_roadmap": "[12-month hiring plan with roles and timelines]",\n'
                '    "data_room_link": "[URL to due diligence materials]"\n'
                '  },\n'
                '  "last_updated": "[Current date in YYYY-MM-DD format]"\n'
                '}\n\n'
                
                "Requirements:\n"
                "1. Create a realistic, investable startup in a growing market\n"
                "2. Use specific numbers, percentages, and data points throughout\n"
                "3. Ensure all financial projections are realistic and achievable\n"
                "4. Include multiple customer personas if relevant to the business\n"
                "5. Reference real market research sources and competitors where possible\n"
                "6. Make the team background compelling with relevant expertise\n"
                "7. Ensure the business model shows clear path to $10M+ revenue\n"
                "8. Include specific, actionable go-to-market tactics\n"
                "9. Address major risks honestly with concrete mitigation plans\n"
                "10. Provide valid JSON that can be parsed programmatically\n\n"
                
                "Focus on emerging technologies or large market disruptions like AI, climate tech, "
                "fintech, healthtech, or B2B SaaS. Make it compelling enough that a VC would want "
                "to schedule a meeting after reading it."
            ),
        },
    ]


# Designate the entry point function
export = unicorn_report