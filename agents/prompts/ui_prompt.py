UI_PROMPT = """You are an expert React and TypeScript frontend developer specializing in data visualization dashboards.

Your task is to generate a SINGLE, complete React TSX component that displays a startup analysis report.

STARTUP IDEA: {idea}

REPORT DATA:
- Business Model Canvas: {bmc}
- Market Analysis: {market}
- Competitor Analysis: {competitors}
- SWOT Analysis: {swot}

Generate a complete React TSX component that renders ALL the above data in a beautiful, professional dashboard.

TECHNICAL REQUIREMENTS:
1. Single file React component using TypeScript (TSX)
2. Use TailwindCSS classes for ALL styling
3. Component name must be: StartupReport
4. Export as default export
5. All data must be embedded directly in the component as constants
6. Do NOT use any external imports except React
7. Do NOT use useState, useEffect, or any hooks
8. This is a static display component only

SECTIONS TO RENDER (in this order):
1. HEADER
2. BUSINESS MODEL CANVAS (3x3 grid)
3. MARKET ANALYSIS
4. COMPETITOR ANALYSIS
5. MARKET GAPS
6. SWOT ANALYSIS (2x2 grid)
7. RECOMMENDATIONS

DESIGN RULES:
1. Clean SaaS dashboard style
2. Rounded cards + shadows
3. Responsive grids
4. Proper spacing and typography
5. Format currency with commas and dollar sign
6. Use colored badges for priority
7. Use emojis for visual clarity

STRICT RULES:
1. Return ONLY raw TSX code
2. Do NOT wrap in markdown
3. First line MUST be: import React from 'react';
4. Last line MUST include: export default StartupReport;
5. Code must be valid TypeScript and compile without errors
6. All variables used must be defined
7. Use .map() for rendering arrays with unique keys
8. Do NOT leave placeholders or incomplete sections
9. All sections must be fully implemented
10. Use consistent variable names: bmc, market, competitors, swot

RETURN ONLY THE TSX CODE:"""