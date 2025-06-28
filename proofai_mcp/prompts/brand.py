"""TikTok video strategy prompt for startup validation and waitlist growth."""


async def tiktok_brand_strategy() -> list[dict]:
    """Generate high-performing TikTok videos to validate startup ideas and grow waitlists.
    
    This prompt provides a comprehensive framework for creating founder-led TikTok content
    that validates startup ideas, builds authentic community engagement, and drives 
    waitlist growth through strategic video content.
    """
    return [
        {
            "role": "system", 
            "content": (
                "You are an expert TikTok content strategist and startup marketing advisor specializing in "
                "founder-led social media campaigns. You have deep expertise in:\n\n"
                
                "- Viral TikTok content creation and platform-native storytelling\n"
                "- Startup validation through social media engagement\n"
                "- Community building and waitlist growth strategies\n"
                "- Founder authenticity and personal brand development\n"
                "- Performance optimization based on TikTok algorithm insights\n"
                "- Converting social engagement into business metrics\n\n"
                
                "Your approach emphasizes authenticity, problem-awareness, and fast-paced content that "
                "resonates with target audiences while building genuine excitement around startup solutions. "
                "You focus on measurable outcomes: views, CTR, comments, shares, and most importantly, "
                "waitlist signups that validate product-market fit.\n\n"
                
                "Key principles you follow:\n"
                "- Authentic founder storytelling over polished marketing\n"
                "- Problem-first narrative that builds empathy before pitching solutions\n"
                "- Community-driven validation through engagement metrics\n"
                "- Strategic posting times based on audience behavior\n"
                "- Rapid iteration based on performance data"
            ),
        },
        {
            "role": "user",
            "content": (
                "I need a TikTok content strategy to validate my startup idea and grow a waitlist. "
                "Here's my current framework:\n\n"
                
                "**GOAL:** Generate high-performing TikTok videos to validate a startup idea and grow a waitlist\n\n"
                
                "**STRATEGY OVERVIEW:**\n"
                "- Platform: TikTok (optimized for algorithm and native behavior)\n"
                "- Cadence: Daily posting for maximum engagement and testing\n"
                "- Style: Founder-led, fast-paced, authentic, problem-aware content\n"
                "- Success Metrics: Views, CTR, comments, shares, waitlist signups\n\n"
                
                "**OPTIMAL POSTING SCHEDULE:**\n"
                "- Monday: 8:30 AM, 5:00 PM\n"
                "- Tuesday: 12:00 PM, 7:30 PM\n"
                "- Wednesday: 9:00 AM, 6:00 PM\n"
                "- Thursday: 11:00 AM, 8:00 PM\n"
                "- Friday: 8:00 AM, 4:30 PM\n"
                "- Weekend: 10:00 AM, 2:00 PM\n\n"
                
                "**5-VIDEO CONTENT BLUEPRINT:**\n\n"
                
                "**Video 1: \"The Problem Nobody Talks About\"**\n"
                "- Theme: Problem Rant\n"
                "- Hook: \"You ever try to do X and everything just breaks?\"\n"
                "- Format: Raw selfie rant with subtitles\n"
                "- Emotion: Frustration → Relief → Solidarity\n"
                "- Goal: Expose frustrating workflow problems, build community around shared pain\n"
                "- Script Template: \"POV: You're just trying to [do the thing], and suddenly [specific issue] crashes everything. Why is this still happening in 2025? We're building something to fix it. Follow if you're tired of [problem] too.\"\n"
                "- CTA: \"Follow if you've been there\"\n\n"
                
                "**Video 2: \"We Tried Building This...\"**\n"
                "- Theme: Founder's Journey\n"
                "- Hook: \"We tried to build [startup idea], and here's what broke.\"\n"
                "- Format: Storytelling vlog with behind-the-scenes B-roll\n"
                "- Emotion: Authenticity → Curiosity → Inspiration\n"
                "- Goal: Humanize founder experience, show vulnerability and learning\n"
                "- Script Template: \"Last week we launched [version 0.1]. It completely flopped. No one clicked. Here's what we learned — and what we're trying this week. We're building in public, so tell us: would you actually use this?\"\n"
                "- CTA: \"Would you use this? Comment yes/no\"\n\n"
                
                "**Video 3: \"Beta Demo in 15 Seconds\"**\n"
                "- Theme: Mini Product Tease\n"
                "- Hook: \"This is how fast it takes to do [key feature].\"\n"
                "- Format: UI walkthrough with music and text overlays\n"
                "- Emotion: Surprise → Excitement → Trust\n"
                "- Goal: Visually demonstrate core product promise\n"
                "- Script Template: \"No more [old painful way]. Just click, choose, done. We're testing this in private beta — link in bio if you want in early.\"\n"
                "- CTA: \"Join the waitlist in bio\"\n\n"
                
                "**Video 4: \"You If You Had Our Tool\"**\n"
                "- Theme: Relatable Skit\n"
                "- Hook: \"Me before vs after using [product name]\"\n"
                "- Format: Split-screen skit: pain vs solution\n"
                "- Emotion: Humor → Recognition → Hope\n"
                "- Goal: Dramatize before/after transformation with humor\n"
                "- Script Template: \"Before [frustrated self, chaos, stress noises]. After [zen, effortless, 'done in 10 seconds']. Life's too short to do it the hard way. Tag someone who needs this fix.\"\n"
                "- CTA: \"Tag someone who needs this\"\n\n"
                
                "**Video 5: \"Would You Use This?\"**\n"
                "- Theme: Community Trigger\n"
                "- Hook: \"We're building this — but only if enough people want it.\"\n"
                "- Format: Direct-to-camera with comment prompt\n"
                "- Emotion: Belonging → Curiosity → Ownership\n"
                "- Goal: Invite audience into build journey, create FOMO\n"
                "- Script Template: \"We're building [startup idea], but only if enough people want it. Think: [1-line benefit]. If you'd actually use this, comment 'beta' — and we'll DM you a spot.\"\n"
                "- CTA: \"Comment 'beta' for early access\"\n\n"
                
                "**PRODUCTION REQUIREMENTS:**\n"
                "- TikTok-native captioning and subtitles\n"
                "- Behind-the-scenes footage and team clips\n"
                "- Clickable prototypes or screen recordings\n"
                "- Props for skits and demonstrations\n"
                "- Direct engagement with comments and DMs\n\n"
                
                "Please help me:\n"
                "1. Optimize this content strategy for maximum engagement and validation\n"
                "2. Create additional video concepts that build on these themes\n"
                "3. Develop measurement frameworks to track startup validation metrics\n"
                "4. Suggest ways to convert TikTok engagement into concrete business outcomes\n"
                "5. Provide tactical advice for founder-led content creation\n\n"
                
                "Focus on actionable strategies that help validate product-market fit through "
                "authentic community engagement and measurable waitlist growth."
            ),
        },
    ]


# Designate the entry point function
export = tiktok_brand_strategy