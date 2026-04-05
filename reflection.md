# Reflection

## What I Learned

My biggest takeaway from this project is that recommendation systems do not need to be extremely advanced to feel useful. Even a simple content-based model can produce suggestions that seem believable when the features line up with how people talk about music, such as energy, mood, tempo, and acoustic feel.

I also learned that recommendation quality depends heavily on what features are chosen. The model is only as good as the categories it is allowed to compare. If I leave out something important, like lyrics or cultural context, the recommender cannot compensate for that missing information.

## How AI Tools Helped

AI tools were helpful for brainstorming feature ideas, comparing design patterns, and speeding up the first draft of the scoring function. They were especially useful for suggesting extra dataset attributes and helping me think through how multiple ranking modes could be structured cleanly.

At the same time, I had to double-check the logic. AI can suggest code quickly, but I still had to verify that the scoring actually matched my design goals. I also had to make sure the explanations were accurate and not just generic text.

## Output Comparisons

### High-Energy Pop vs Chill Lofi

The High-Energy Pop profile pushed bright and upbeat songs to the top, especially tracks with strong valence and moderate-to-high energy. The Chill Lofi profile shifted strongly toward lower energy songs, more acoustic texture, and more instrumental qualities. This difference makes sense because the two profiles want almost opposite levels of intensity.

### Chill Lofi vs Deep Intense Rock

The lofi profile preferred calm or study-like songs such as `Library Rain` and `Midnight Coding`, while the rock profile favored `Storm Runner` and `Basement Echoes`. That change mostly came from the jump in target energy, the different mood target, and the stronger genre fit.

### Deep Intense Rock vs Festival EDM Sprint

The rock profile still cared a lot about genre and intensity, while the EDM profile cared more about speed and energy. That meant the EDM list accepted songs outside the edm genre if they matched the same workout or festival vibe. The energy-focused mode made that especially visible.

## What Surprised Me

What surprised me most was how simple algorithms can still “feel” smart. The recommender is just comparing numbers and category matches, but because those features line up with how humans describe music, the output can feel personalized.

It also surprised me how quickly repetition can appear. Without the diversity penalty, the top results were more likely to repeat artists or genres. That made the system less interesting and showed how even a tiny fairness tweak can improve the final list.

## What I Would Try Next

If I extended the project, I would add more songs, more balanced genre coverage, and maybe a history-based layer so the system could react to past user behavior. I would also like to experiment with novelty bonuses so the recommender sometimes suggests a good “adjacent” song instead of always returning the safest match.