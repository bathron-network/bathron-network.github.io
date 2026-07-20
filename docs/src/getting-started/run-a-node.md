# Run a node

> The network currently runs as a **private testnet**. You can build and run the node today;
> published peers, genesis and a distribution faucet ship with the **public testnet**—the next
> milestone. The faucet distributes units originating from prior testnet-BTC burns; it has no
> mint key and cannot bypass the accounting invariants. [Contact us](mailto:contact@bathron.org)
> if you want early access.

## Build from source

On Debian/Ubuntu:

```bash
sudo apt-get install -y build-essential libtool autotools-dev automake pkg-config \
    libssl-dev libevent-dev bsdmainutils python3 libboost-all-dev libsodium-dev libzmq3-dev

./autogen.sh
./configure --without-gui --disable-tests --disable-bench
make -j$(nproc)
```

This produces two binaries:

| Binary | Role |
|---|---|
| `bathrond` | the node daemon |
| `bathron-cli` | command-line RPC client |

## Run

```bash
bathrond -testnet -daemon
```

The node stores its data in `~/.bathron/`. Configuration goes in `~/.bathron/bathron.conf` (peers, RPC credentials).

## Verify

```bash
bathron-cli -testnet getblockcount        # chain height
bathron-cli -testnet getstate             # global settlement state + invariants
bathron-cli -testnet getfinalitystatus    # finality lag (healthy = 0)
bathron-cli -testnet getbtcheadersstatus  # in-consensus Bitcoin header chain
```

A healthy node produces a new block every 60 seconds network-wide, finalizes with lag 0, and tracks the Bitcoin header chain inside consensus.
