# Hackathon Quick Start Guide

Get started with the AgriConnect Hackathon Environment in 5 minutes.

## Installation

You're already set up! The environment is in `hackathon/` directory.

## First Agent (5 min)

### 1. Create Basic Script

Create `my_agent.py`:

```python
from hackathon.env import HackathonEnv

# Create environment
env = HackathonEnv(agent_type='farmer')

# Start episode
state = env.reset(task_id='farmer_maximize_revenue')

# Take 100 steps
for step in range(100):
    # Simple policy: add produce on odd steps, accept orders on even
    if step % 2 == 0:
        action = {
            'action_type': 'add_produce',
            'produce_name': 'Tomato',
            'quantity': 100,
            'price': 50,
        }
    else:
        # Try to accept first pending order
        for order in state.active_orders:
            if order.status == 'pending':
                action = {
                    'action_type': 'accept_order',
                    'target_order_id': order.id,
                }
                break
        else:
            action = {'action_type': 'noop'}
    
    # Execute action
    state, reward, done, info = env.step(action)
    
    if step % 10 == 0:
        print(f"Step {step}: Reward={reward:.2f}")
    
    if done:
        break

print(f"Episode complete! Total steps: {env.step_count}")
```

### 2. Run It

```bash
python my_agent.py
```

### 3. See Results

You'll see rewards printed every 10 steps. Adjust the policy to improve!

## Key Concepts (2 min read)

### State: What you observe

```python
state = env.state()
# Access information:
state.farmers           # List of farmers on platform
state.restaurants       # List of restaurants
state.produce_items     # Available produce items
state.active_orders     # Current orders
state.platform_metrics  # Overall platform stats
```

### Action: What you do

**Farmer actions:**
```python
# Add produce to sell
{'action_type': 'add_produce', 'produce_name': 'Tomato', 'quantity': 100, 'price': 50}

# Accept an incoming order
{'action_type': 'accept_order', 'target_order_id': 123}

# Do nothing
{'action_type': 'noop'}
```

**Restaurant actions:**
```python
# Request produce from farmer
{'action_type': 'request_produce', 'produce_id': 456, 'quantity': 50}

# Do nothing
{'action_type': 'noop'}
```

### Step: What happens

```python
state, reward, done, info = env.step(action)
# state: Updated environment state
# reward: How good was this action? (higher is better)
# done: Is episode finished?
# info: Detailed information about what happened
```

## 5-Minute Challenge

Build a restaurant agent that requests produce from at least 3 different farmers:

```python
from hackathon.env import HackathonEnv

env = HackathonEnv(agent_type='restaurant')
state = env.reset(task_id='restaurant_build_network')

farmers_requested = set()

for step in range(100):
    # Find produce from farmer we haven't requested from yet
    action = None
    for produce in state.produce_items:
        if produce.farmer_id not in farmers_requested:
            action = {
                'action_type': 'request_produce',
                'produce_id': produce.id,
                'quantity': 20,
            }
            farmers_requested.add(produce.farmer_id)
            break
    
    if action is None:
        action = {'action_type': 'noop'}
    
    state, reward, done, info = env.step(action)
    
    if done or len(farmers_requested) >= 3:
        break

print(f"Requested from {len(farmers_requested)} farmers!")
```

## Understanding Rewards

Rewards increase when you:

**Farmer:**
- Accept orders (+10)
- Generate revenue (+0.01 per $)
- Improve trust score (+1 per point)
- Reduce spoilage (-penalty)
- Keep freshness high (+0.5 per point)

**Restaurant:**
- Place orders (+5)
- Get orders fulfilled (+10)
- Diversify suppliers (+2 per new farmer)
- Negotiate prices (-penalty for excess)
- Get fresh produce (+1 per point)

## Available Tasks

### Farmer Tasks
- `farmer_maximize_revenue`: Make as much money as possible
- `farmer_build_reputation`: Build trust and good reviews
- `farmer_optimize_availability`: Keep produce fresh and available

### Restaurant Tasks
- `restaurant_build_network`: Connect with many farmers
- `restaurant_minimize_costs`: Get best prices
- `restaurant_guarantee_freshness`: Receive quality produce

## Debugging Tips

### 1. Print state details

```python
print(f"Farmers: {len(state.farmers)}")
print(f"Available produce: {len(state.produce_items)}")
print(f"Pending orders: {len([o for o in state.active_orders if o.status == 'pending'])}")
```

### 2. Check action results

```python
output = env.step(action)
print(f"Success: {output.info['action_result'].get('success')}")
print(f"Reward: {output.reward}")
print(f"Error: {output.info['action_result'].get('error')}")
```

### 3. Track cumulative reward

```python
total_reward = 0
for step in range(100):
    # ... your action logic
    state, reward, done, info = env.step(action)
    total_reward += reward
    print(f"Step {step}: Reward={reward:.2f}, Total={total_reward:.2f}")
```

## Next Steps

1. **Run examples:** `python usage_example.py` (in hackathon/ dir)
2. **Look at tests:** `test_env.py` for more patterns
3. **Read full docs:** `README.md` for complete API
4. **Build something cool:** Create a smarter policy and compete!

## Common Questions

**Q: Where do I put my agent code?**  
A: Create your own Python file, or add to `my_agent.py`

**Q: Can I use ML frameworks?**  
A: Yes! Use TensorFlow, PyTorch, scikit-learn, etc.

**Q: How do I get task scores?**  
A: After episode ends with `done=True`, check `output.task_progress` for evaluation

**Q: Can I reset mid-episode?**  
A: Yes, call `env.reset()` anytime to start fresh

**Q: How many steps can I run?**  
A: Default is 100 steps per episode, configurable

## File Structure

```
hackathon/
├── env.py               ← Main environment (read this second)
├── schemas.py           ← Data types
├── tasks.py             ← Task definitions
├── rewards.py           ← Reward calculations
├── usage_example.py     ← Example code (start here!)
├── test_env.py          ← Test cases
├── README.md            ← Full documentation
└── QUICK_START.md       ← This file
```

## Ready to Start?

Create a file `my_agent.py` and copy the 5-minute example above. Run it with:

```bash
python my_agent.py
```

Good luck! 🚀

---

**Need help?** Check `README.md` or look at `usage_example.py` for more patterns.
