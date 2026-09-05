# Runtime role policy

The container is an execution boundary, not an authority source. Its JSON
assignment transports an already approved task; it cannot choose a task,
expand permitted paths, merge, or promote governance state.

The host verifies the role's GitHub login before cloning. Author mode may
checkpoint only the assigned non-protected branch. Reviewer mode mounts
source read-only and permits publication of exact-head review metadata only.
The host verifies review evidence before disposal and never pushes the
author's branch from a reviewer cycle.

The worker's numeric UID/GID match the owning WSL user, with the container
account named `agent`. There is no writable shared Git metadata or persistent
package volume. Provider authentication state is scoped to one role; Google
credentials stay on the host. Network policy is explicit, exact-host HTTPS
allowlisting through a proxy on an isolated worker network.

The controller does not replace GitHub branch protection, repository-scoped
tokens, approved task routing or the project's formal review publisher.
See [the runtime contract](../README.md) for lifecycle, recovery and limitations.
