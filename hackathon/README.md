# AgriConnect Hackathon Environment

A comprehensive OpenEnv-compatible environment for AgriConnect hackathon challenges, enabling participants to build AI agents that interact with a dynamic platform connecting farmers and restaurants.

## Overview

The AgriConnect Hackathon Environment (`HackathonEnv`) is the core interface for engaging with the platform. It provides:

- **Multi-agent simulation**: Farmer and restaurant agents operating in parallel
- **Real-world challenges**: Tasks that reflect actual AgriConnect operations
- **Reward-based learning**: Structured reward signals for reinforcement learning
- **Observable state**: Complete platform state including market data
- **Benchmarked evaluation**: Scientific task grading with reproducible metrics

## Quick Start

### Installation

1. Ensure Django project is set up (`backend/` directory)
2. All dependencies are in `requirements.txt`
3. Database should be initialized with migrations

### Basic Usage

```python
from hackathon.env import HackathonEnv

# Create environment for farmer agent
env = HackathonEnv(agent_type='farmer')

# Reset to start episode
state = env.reset(task_id='farmer_maximize_revenue')

# Take steps in environment
for step in range(100):
    action = your_agent_policy(state)
    state, reward, done, info = env.step(action)
    
    if done:
        print(f"Episode complete! Total reward: {sum(env.episode_rewards)}")
        break
```

## Architecture

### Main Components

```
hackathon/
├── env.py                    # Core HackathonEnv class
├── schemas.py               # Pydantic data models
├── tasks.py                 # Task definitions and grading
├── rewards.py               # Reward calculation logic
├── services.py              # Business logic services
├── test_env.py              # Unit tests
├── usage_example.py         # Usage examples
└── README.md                # This file
```

### Data Flow

```
User Action
    ↓
env.step(action)
    ↓
_execute_action() → Database Updates
    ↓
_get_state() → Platform State
    ↓
RewardCalculator → Reward Signal
    ↓
TaskGrader → Task Progress (if complete)
    ↓
StepOutput (state, reward, done, task_progress)
```

## API Reference

### HackathonEnv Class

#### Initialization

```python
env = HackathonEnv(
    agent_type: str = 'farmer',      # 'farmer' or 'restaurant'
    agent_id: Optional[int] = None,  # User ID (None = auto-create)
    simulation_mode: bool = True     # Use simulation or live DB
)
```

#### Methods

##### `reset(task_id: Optional[str] = None) -> EnvironmentState`

Reset environment and start new episode.

**Parameters:**
- `task_id`: Task identifier (see Tasks section). If None, selects default task for agent type.

**Returns:** `EnvironmentState` containing initial state

**Example:**
```python
state = env.reset(task_id='farmer_maximize_revenue')
```

##### `state() -> EnvironmentState`

Get current environment state without taking action.

**Returns:** Current `EnvironmentState`

**Example:**
```python
current_state = env.state()
print(f"Active orders: {len(current_state.active_orders)}")
```

##### `step(action: Dict[str, Any]) -> StepOutput`

Execute action and observe results.

**Parameters:**
- `action`: Dictionary with:
  - `action_type` (str): Type of action to execute
  - Additional parameters depending on action type

**Returns:** `StepOutput` containing:
- `state`: Updated `EnvironmentState`
- `reward`: Float reward for this step
- `done`: Boolean indicating episode completion
- `info`: Dictionary with additional information
- `task_progress`: Task evaluation (if episode done)

**Example:**
```python
output = env.step({
    'action_type': 'add_produce',
    'produce_name': 'Tomato',
    'quantity': 100,
    'price': 50,
})
```

### Data Models (schemas.py)

#### EnvironmentState

Complete state snapshot of the platform.

```python
@dataclass
class EnvironmentState:
    step_count: int
    timestamp: str
    farmers: List[FarmerSnapshot]
    restaurants: List[RestaurantSnapshot]
    produce_items: List[ProduceSnapshot]
    active_orders: List[OrderSnapshot]
    platform_metrics: Dict[str, float]
```

#### FarmerSnapshot

Snapshot of a farmer's status.

```python
@dataclass
class FarmerSnapshot:
    user_id: int
    username: str
    total_produce: int
    available_produce: int
    trust_score: float
    total_orders: int
    completed_orders: int
```

#### RestaurantSnapshot

Snapshot of a restaurant's status.

```python
@dataclass
class RestaurantSnapshot:
    user_id: int
    username: str
    total_orders: int
    completed_orders: int
    trust_score: float
    total_spending: float
    pending_orders: int
```

#### ProduceSnapshot

Snapshot of a produce item.

```python
@dataclass
class ProduceSnapshot:
    id: int
    name: str
    quantity: float
    price_per_kg: float
    freshness_score: float
    spoilage_risk: float
    produce_state: str
    days_until_expiry: Optional[int]
```

#### OrderSnapshot

Snapshot of an order.

```python
@dataclass
class OrderSnapshot:
    id: int
    status: str
    quantity: float
    total_price: float
    produce_name: str
    farmer_id: int
    restaurant_id: int
    days_pending: Optional[int]
```

#### StepOutput

Complete output of a step.

```python
@dataclass
class StepOutput:
    state: EnvironmentState
    reward: float
    done: bool
    info: Dict[str, Any]
    task_progress: Optional[Dict[str, Any]]
```

## Actions

### Farmer Actions

#### `accept_order`

Accept an incoming order from a restaurant.

```python
action = {
    'action_type': 'accept_order',
    'target_order_id': 123,  # Order ID to accept
}
```

**Reward:** Order acceptance reward + fulfillment potential

#### `add_produce`

Add new produce to inventory.

```python
action = {
    'action_type': 'add_produce',
    'produce_name': 'Tomato',
    'quantity': 100,           # kg
    'price': 50,              # per kg
}
```

**Reward:** Inventory expansion reward

### Restaurant Actions

#### `request_produce`

Request produce from a farmer.

```python
action = {
    'action_type': 'request_produce',
    'produce_id': 456,         # Produce item ID
    'quantity': 50,            # kg requested
}
```

**Reward:** Order placement reward

## Tasks

### Farmer Tasks

#### `farmer_maximize_revenue`

**Objective:** Maximize revenue in 100 steps

**Metrics:**
- Total revenue generated
- Number of completed orders
- Average order fulfillment rate

**Success Criteria:**
- Revenue > $5000
- Completed orders > 20
- Fulfillment rate > 80%

**Example:**
```python
state = env.reset(task_id='farmer_maximize_revenue')
# Complete the task to earn reward
```

#### `farmer_build_reputation`

**Objective:** Build trust score and reputation

**Metrics:**
- Trust score improvement
- Customer satisfaction
- Spoilage rate minimization

**Success Criteria:**
- Trust score > 8.5
- Spoilage rate < 10%
- Repeat customer rate > 50%

#### `farmer_optimize_availability`

**Objective:** Maintain high produce availability

**Metrics:**
- Average availability per product
- Inventory turnover rate
- Freshness score maintenance

**Success Criteria:**
- Avg availability > 85%
- Turnover > 2x per week
- Avg freshness > 8.0

### Restaurant Tasks

#### `restaurant_build_network`

**Objective:** Establish relationships with multiple farmers

**Metrics:**
- Number of unique farmer suppliers
- Network stability
- Average supplier trust score

**Success Criteria:**
- Working with >10 farmers
- Network stability > 80%
- Avg supplier trust > 7.5

#### `restaurant_minimize_costs`

**Objective:** Get best prices from suppliers

**Metrics:**
- Average unit cost
- Cost per order
- Savings vs baseline

**Success Criteria:**
- Avg cost/kg < $45
- Cost per order < $1000
- Cost savings > 20%

#### `restaurant_guarantee_freshness`

**Objective:** Ensure high freshness of received produce

**Metrics:**
- Avg freshness score of received items
- Rejection rate for poor quality
- Customer satisfaction

**Success Criteria:**
- Avg freshness > 8.5
- Rejection rate < 5%
- Satisfaction > 90%

## Reward Calculation

### Reward Components

**Farmer Rewards:**
1. Order acceptance reward: +10 pts
2. Revenue reward: +0.01 per dollar earned
3. Reputation reward: +1 per trust point gained
4. Efficiency reward: -1 per 1% spoilage above threshold
5. Freshness reward: +0.5 per 0.1 point above 8.0

**Restaurant Rewards:**
1. Order placement reward: +5 pts
2. Fulfillment reward: +10 per order fulfilled
3. Supplier diversity reward: +2 per unique farmer (capped)
4. Cost efficiency reward: -0.01 per dollar over budget
5. Quality reward: +1 per 0.1 point freshness above 8.0

### Calculation Example

```python
# Step-by-step reward for farmer accepting order
base_reward = 10  # Accept order
revenue_gain = 500 * 0.01 = 5  # Revenue component
trust_gain = 0.3 * 1 = 0.3     # Reputation component
spoilage_penalty = -2           # Spoilage above 5%
total = 10 + 5 + 0.3 - 2 = 13.3 points
```

## Task Grading

After episode completion, task performance is graded:

```python
task_eval = output.task_progress
# {
#     'success': bool,              # Whether success criteria met
#     'score': float,               # Score from 0-100
#     'reward_earned': float,       # Bonus reward for success
#     'metrics': {                  # Detailed metrics
#         'metric_name': value,
#         ...
#     }
# }
```

## Examples

### Example: Simple Farmer Agent

```python
from hackathon.env import HackathonEnv

def farmer_policy(state):
    """Simple farmer policy: add produce regularly"""
    if len(state.active_orders) < 5:
        return {
            'action_type': 'add_produce',
            'produce_name': 'Tomato',
            'quantity': 100,
            'price': 50,
        }
    else:
        # Accept first pending order
        for order in state.active_orders:
            if order.status == 'pending':
                return {
                    'action_type': 'accept_order',
                    'target_order_id': order.id,
                }
    
    return {'action_type': 'noop'}

# Run episode
env = HackathonEnv(agent_type='farmer')
state = env.reset(task_id='farmer_maximize_revenue')

total_reward = 0
for step in range(100):
    action = farmer_policy(state)
    output = env.step(action)
    
    total_reward += output.reward
    state = output.state
    
    if output.done:
        print(f"Episode complete!")
        if output.task_progress:
            print(f"Task success: {output.task_progress['success']}")
            print(f"Score: {output.task_progress['score']:.2f}/100")
        break

print(f"Total reward: {total_reward:.2f}")
```

### Example: Multi-Agent Simulation

```python
from hackathon.env import HackathonEnv

# Create environments for both agent types
farmer_env = HackathonEnv(agent_type='farmer')
restaurant_env = HackathonEnv(agent_type='restaurant')

# Reset both
farmer_state = farmer_env.reset()
restaurant_state = restaurant_env.reset()

# Simulate interaction
for step in range(50):
    # Restaurant requests produce
    if restaurant_state.produce_items:
        produce = restaurant_state.produce_items[0]
        rest_action = {
            'action_type': 'request_produce',
            'produce_id': produce.id,
            'quantity': 50,
        }
        rest_output = restaurant_env.step(rest_action)
        restaurant_state = rest_output.state
    
    # Farmer accepts orders
    farmer_action = {
        'action_type': 'add_produce',
        'produce_name': 'Tomato',
        'quantity': 100,
        'price': 50,
    }
    farmer_output = farmer_env.step(farmer_action)
    farmer_state = farmer_output.state
    
    print(f"Step {step+1}: Farmer reward={farmer_output.reward:.2f}, "
          f"Restaurant reward={rest_output.reward:.2f}")
```

## Testing

Run unit tests:

```bash
python manage.py test hackathon.test_env
```

Run specific test:

```bash
python manage.py test hackathon.test_env.TestHackathonEnv.test_step_returns_step_output
```

## Advanced Usage

### Custom Reward Weights

Modify `rewards.py` to customize reward calculations:

```python
# In rewards.py
REWARD_WEIGHTS = {
    'order_acceptance': 15,      # Increase from 10
    'revenue_factor': 0.015,     # Increase from 0.01
    'spoilage_penalty': -3,      # Increase penalty
}
```

### Multi-Step Planning

Use environment for episodic planning:

```python
def plan_episode(env, agent_type):
    """Plan an optimal episode strategy"""
    state = env.reset()
    trajectory = []
    
    for step in range(10):
        # Sample multiple actions
        best_action = None
        best_reward = float('-inf')
        
        for action in generate_candidate_actions(state):
            # Simulate action
            test_output = env.step(action)
            if test_output.reward > best_reward:
                best_reward = test_output.reward
                best_action = action
        
        trajectory.append(best_action)
    
    return trajectory
```

## Troubleshooting

### Issue: "User matching query does not exist"
- Ensure `agent_id` points to valid user
- Use `agent_id=None` to auto-create test user

### Issue: "Produce not found"
- Ensure produce exists before requesting
- Check produce status is 'available'

### Issue: "High spoilage rate"
- Reduce days until expiry in produce
- Check `freshness_score` calculation

## Performance Considerations

- **State size:** Each state includes ~50 objects; typical memory ~5MB
- **Step time:** ~100ms per step (DB operations)
- **Parallel envs:** Can run ~10 environments in parallel on standard hardware
- **Scaling:** For 100+ parallel envs, use database connection pooling

## Future Extensions

1. **Visual debugging:** Matplotlib visualization of state
2. **Replay system:** Save and replay episodes
3. **Curriculum learning:** Progressive task difficulty
4. **Multi-objective:** Pareto frontier evaluation
5. **Transfer learning:** Domain transfer between farmer/restaurant

## Contributing

To extend the environment:

1. Add new actions in `_execute_farmer_action()` or `_execute_restaurant_action()`
2. Update reward weights in `rewards.py`
3. Add new tasks in `tasks.py`
4. Write tests in `test_env.py`
5. Document in this README

## API Summary

| Method | Input | Output | Purpose |
|--------|-------|--------|---------|
| `reset()` | task_id | EnvironmentState | Start new episode |
| `state()` | - | EnvironmentState | Get current state |
| `step()` | action | StepOutput | Execute action |

| Action Type | Agent | Parameters | Effect |
|------------|-------|-----------|--------|
| `accept_order` | Farmer | target_order_id | Accept incoming order |
| `add_produce` | Farmer | name, qty, price | Add to inventory |
| `request_produce` | Restaurant | produce_id, qty | Create order |

## License

AgriConnect Hackathon Environment - Internal Use

---

**For support or questions, contact the hackathon organizers.**
