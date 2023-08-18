# arkose-capsolver
A simple HTTP server to fetch arkose tokens using the CapSolver API.  
Supports concurrent requests to the public token service to enhance redundancy and response speed.  
<br />Note: CapSolver is a paid service, at $2 / 1000 tokens.  
Note 2: This project is for obtaining arkose tokens required when asking questions on OpenAI ChatGPT.  
Note 3: Due to CapSolver’s sometimes suboptimal recognition accuracy, the wait time might be long. It is not recommended for scenarios with high token demand.

## Installation

```
pip3 install capsolver
git clone https://github.com/turfintl/arkose-capsolver.git
```
Edit the `main.py` file and insert your API key.  
(Optional) Uncomment and assign a value to `public_pool_urlx` in the `get_first_result` function to enable support for the public token pool.  
~~(Further) By commenting out capsolver and adding multiple public token pools, it could even transform into a relatively stable local free token service. However, I don’t recommend doing this.~~

## Running

```
python3 main.py
```

## Fetching arkose token
Visit [http://127.0.0.1:8999/token](http://127.0.0.1:8999/token)

## Support

If you find this project helpful, you're welcome to register and use it via the invitation link below:  
[CapSolver Registration Link](https://dashboard.capsolver.com/passport/register?inviteCode=lhn2_FmvyM-N)
