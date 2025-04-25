# 📊 Competitor Analysis – Tennis Video Analytics Tools

This document provides a comparison of existing tennis analytics tools to identify gaps and justify the design of this local-first system.

---

## Competitor Tools Overview

| Product         | Platform     | Price                 | Features                                                                                         | Local Processing | Offline Support | Export Annotated Video | Custom Model Support |
|-----------------|--------------|------------------------|--------------------------------------------------------------------------------------------------|------------------|------------------|--------------------------|-----------------------|
| [SwingVision](https://swing.vision) | iOS          | $180/year (Pro)       | Stroke recognition, line calling, stats dashboard, ball speed, Apple Watch support              | ❌ Cloud-based    | ❌ No             | ✅ Yes                    | ❌ No                  |
| [TennisViz (Hawk-Eye)](https://tennisviz.com) | Pro hardware | $$$$ (Enterprise)     | Broadcast-grade line calling, pro analytics, AI tracking                                         | ❌               | ❌               | ✅                        | ❌                   |
| [Playsight](https://playsight.com) | Hardware + App | $$$ (Per court setup) | Live streaming, multi-angle replay, player stats                                                 | ❌               | ❌               | ✅                        | ❌                   |
| [AI Sports](https://www.ai-sports.tech/) | Android, iOS | Subscription          | Stroke classification, match summaries, player tracking                                          | ❌ Cloud-based    | ❌               | ❌                        | ❌                   |
| **This Project (Local System)** | Desktop App | ✅ Free + Local        | Shot classification, pose estimation, ball tracking, in/out call, download annotated video       | ✅ Fully Local    | ✅ Yes           | ✅ Yes                    | ✅ Future planned     |

---


## Key Differences

- **Privacy-first**: Unlike competitors, this system does not upload your videos to the cloud.
- **Cost-effective**: No subscriptions, just open-source tools.
- **Customizable**: You can plug in your own models, experiment with new features, and debug freely.
- **Offline Use**: Great for places without internet access or users who prefer offline systems.


## Future Consideration
- TBD

---

*Last updated: April 2025 by Stephen*