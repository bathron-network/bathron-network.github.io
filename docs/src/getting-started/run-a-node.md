# Run a node

> The **public testnet is live**. A published seed node and a fixed genesis are available, and a
> fresh node can join with only the seed address — no RPC access and no operator address are
> needed. There is no mainnet. This is experimental software with a disposable-genesis testnet.

## Join the public testnet

| Fact | Value |
|---|---|
| Genesis (block 0) | `0d241620b8beb492fd21bd8a92295260a4afa1b82e1bd816d18323cc3c98ea71` |
| Public seed | `57.131.33.151:27171` |

```bash
mkdir -p ~/.bathron
printf 'testnet=1\n[test]\naddnode=57.131.33.151\n' > ~/.bathron/bathron.conf
bathrond -testnet -daemon
bathron-cli -testnet getblockhash 0
# expected:
# 0d241620b8beb492fd21bd8a92295260a4afa1b82e1bd816d18323cc3c98ea71
bathron-cli -testnet getblockcount   # syncs to the network tip
```

RPC is loopback-only by default. Operator addresses are deliberately not published; the seed
above is the only endpoint needed to join.

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

The node stores its data in `~/.bathron/`. Configuration goes in `~/.bathron/bathron.conf` (peers, RPC credentials). Pre-built binaries for tagged releases are published on the
[bathron-core releases page](https://github.com/bathron-network/bathron-core/releases).

## Verify

```bash
bathron-cli -testnet getblockcount        # chain height
bathron-cli -testnet getstate             # global settlement state + invariants
bathron-cli -testnet getfinalitystatus    # finality lag (healthy = 0)
bathron-cli -testnet getbtcheadersstatus  # in-consensus Bitcoin header chain
```

A healthy node produces a new block every 60 seconds network-wide, finalizes with lag 0, and tracks the Bitcoin header chain inside consensus.

> **During the initial sync, a scary-looking finality status is normal.** While the
> node is still downloading blocks, `getfinalitystatus` can report
> `last_finalized_height: 0` and `status: "critical"`. Finality certificates are
> received *live*: the node catches up on blocks first, then finalizes the current
> tip as soon as the first live certificate arrives. Nothing is wrong with the
> network — the node simply hasn't heard a certificate yet.
>
> Consider the node healthy only once **all** of the following hold: the tip matches
> the network height, a new block has been received, a finality certificate has been
> observed, and `finality_lag` is back to `0`.
