"""Minimal retrieval stub; user must come from server-side authentication."""


def search_chunks(user, query):
    """Build the mandatory tenant filter from the authenticated user."""
    tenant_filter = {"term": {"tenant_id": user.tenant_id}}
    # The Elasticsearch hybrid search call goes here, using tenant_filter.
    raise NotImplementedError("Connect self-hosted Elasticsearch with tenant_filter")
