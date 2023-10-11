---
title: "Migrating from a Single Package Cargo Crate to a Workspace"
layout: post
---

In Rust, we usually have single packages per repository when we start working 
on a project. As our project grows, we might want to have multiple independent 
packages in the same folder/repository, but publish them as separate crates.
Cargo supports this using `workspaces`. But while there is a lot written about 
how to create a new single-package project or a new workspace project, there 
isn't a lot of information on how to turn a single package project into a 
multiproject workspace further down the line.


Lets assume you have a single package Rust project with the following layout:

```
├── Cargo.lock
├── Cargo.toml
├── src
│   ├── lib.rs
│   └── main.rs
└── target 
    ├── debug
    └── release
```

with a `Cargo.toml` that looks like:
```
[package]
name = "awesome_cli"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0.0", features = ["derive"]}

[profile.release]
opt-level = "z"

```

This is our `awesome_cli` tool that we're working on. But now we see that 
there's functionality that we're working on that could be independently useful, 
for instance we wrote great rendering code to make pretty terminal UIs that 
could be used by other projects as well.
So what we'd like is to have two independent packages, `awesome_cli` and 
`awesome_tui`, in a cargo workspace.

Unfortunately, there is no automated way to do this currently, but luckily 
doing it manually isn't hard at all.

We start by creating an `awesome_cli` folder in the root of our project and 
moving the `Cargo.toml` file and `src` folder to this new folder (Note that we 
do not move the `Cargo.lock` file).

Next, we create a new `Cargo.toml` in our top level folder with the following 
content:
```
[workspace]

members = ["awesome_cli"]
```

Since our original `Cargo.toml` has a `[profile.release]` entries in it, we 
have to put them in this new `Cargo.toml` instead, as build profiles have to be 
specified at the workspace level.

At this point, our top level `Cargo.toml` looks like this:
```
[workspace]

members = ["awesome_cli"]

[profile.release]
opt-level = "z"
```
and our `awesome_cli/Cargo.toml` looks like:
```

[package]
name = "awesome_cli"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0.0", features = ["derive"]}
```

At this point, we already have a fully working workspace project, so we can 
move ahead with extracting the TUI features we want into a new package.
```
$ cargo new --lib awesome_tui
```

This creates a new lib package in our workspace. We can now copy over all 
relevant code to the `awesome_tui/lib.rs` file, separating it from our 
`awesom_cli/` code.
We still need to update the dependencies in `awesome_cli` by adding the 
appropriate `use awesome_tui::*` imports, as well as adding the new package to 
our workspace `Cargo.toml`. For convenience, we'll also add our new package as 
a workspace dependency so we can easily import it:
```
[workspace]

members = ["awesome_cli", "awesome_tui"]

[workspace.dependencies]
awesome_tui = { path = "./awesome_tui", version = "0.1.0" }

[profile.release]
opt-level = "z"
```

and in our `awesome_cli/Cargo.toml` we'll add it as a dependency as well:
```
[package]
name = "awesome_cli"
version = "0.1.0"
edition = "2021"

[dependencies]
serde = { version = "1.0.0", features = ["derive"]}
awesome_tui = { workspace = true}
```
The `workspace = true` part just tells our package to use the dependency 
defined at the top/workspace level.

That's it. You now have a functioning cargo workspace and you can build/publish 
your packages separately!



