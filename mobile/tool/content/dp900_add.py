"""DP-900 additions to align weighting to the study guide and fill gaps.

Brings the analytics domain back under its 30% ceiling by deepening core,
relational, and non-relational coverage, and adds the Azure Data Factory and
Azure Cosmos DB API items the legacy coverage missed.
"""

SRC = (
    "Original AI-fleet-authored content; publisher substantive review PENDING (Dimitri Meier); "
    "facts from Microsoft Learn DP-900 study guide (2026-07-21) and docs, "
    "retrieved 2026-10-02"
)
BASIS = "original-human-ai-assisted"
COURSE = "dp-900"

_DOMAIN = {
    "core": "Core Data Concepts",
    "rel": "Relational Data on Azure",
    "nonrel": "Non-relational Data on Azure",
    "analytics": "Analytics Workload",
}


def q(id_, domain, text, options, ci, expl, diff="medium"):
    return {
        "id": id_,
        "text": text,
        "options": options,
        "correctOptionIndex": ci,
        "explanation": expl,
        "domain": _DOMAIN[domain],
        "difficulty": diff,
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    }


QUESTIONS = [
    q("dp-900-047", "core",
      "Which file format is a compact, row-based binary format often used for "
      "data serialization?",
      ["Avro", "CSV", "JSON", "XML"],
      0,
      "Avro is a compact, row-based binary format commonly used for data "
      "serialization.",
      "medium"),
    q("dp-900-048", "core",
      "Which characteristic distinguishes semi-structured data from "
      "structured data?",
      ["It has a flexible or self-describing schema",
       "It always lives in a relational table",
       "It has no organization at all",
       "It can only be stored as binary"],
      0,
      "Semi-structured data has a flexible or self-describing schema (for "
      "example JSON), unlike the fixed schema of structured data.",
      "medium"),
    q("dp-900-049", "core",
      "Which type of data store stores records as objects or documents with "
      "no fixed relational schema?",
      ["A document store",
       "A relational database",
       "A data warehouse",
       "A file share"],
      0,
      "A document store keeps records as documents (often JSON) with no "
      "fixed relational schema.",
      "medium"),
    q("dp-900-050", "core",
      "Which workload requires atomic, consistent, isolated, durable (ACID) "
      "transactions on current data?",
      ["A transactional workload",
       "An analytical workload",
       "A batch job",
       "An archive job"],
      0,
      "Transactional workloads rely on ACID transactions over current data, "
      "whereas analytical workloads aggregate historical data.",
      "medium"),
    q("dp-900-051", "rel",
      "Which SQL statement changes values in existing rows of a table?",
      ["UPDATE", "SELECT", "INSERT", "CREATE"],
      0,
      "UPDATE modifies values in existing rows; INSERT adds rows, SELECT "
      "reads rows, and CREATE defines objects.",
      "medium"),
    q("dp-900-052", "rel",
      "Which database object is used to speed up lookups on a column?",
      ["An index", "A view", "A stored procedure", "A primary key"],
      0,
      "An index speeds up lookups on a column, at the cost of extra storage "
      "and write overhead.",
      "medium"),
    q("dp-900-053", "rel",
      "What does a foreign key define in a relational database?",
      ["A reference to the primary key of another table",
       "A unique value for every row",
       "A saved query",
       "A permission grant"],
      0,
      "A foreign key references the primary key of another table, defining a "
      "relationship between tables.",
      "medium"),
    q("dp-900-054", "nonrel",
      "Which Azure Cosmos DB API is compatible with MongoDB?",
      ["MongoDB API", "Core (SQL) API", "Gremlin API", "Table API"],
      0,
      "The MongoDB API in Azure Cosmos DB lets applications use MongoDB "
      "drivers and query patterns.",
      "medium"),
    q("dp-900-055", "nonrel",
      "Which Azure Cosmos DB API is compatible with Apache Cassandra?",
      ["Cassandra API", "Core (SQL) API", "Gremlin API", "MongoDB API"],
      0,
      "The Cassandra API in Azure Cosmos DB supports Cassandra Query Language "
      "and column-family data.",
      "medium"),
    q("dp-900-056", "nonrel",
      "Which type of Azure Blob is optimized for appending data such as log "
      "entries?",
      ["Append blobs", "Block blobs", "Page blobs", "Queue blobs"],
      0,
      "Append blobs are optimized for appending data such as log entries; "
      "block blobs suit general binary/text, and page blobs suit disks.",
      "medium"),
    q("dp-900-057", "analytics",
      "Which service orchestrates and schedules data movement and "
      "transformation pipelines in Azure?",
      ["Azure Data Factory", "Azure Cosmos DB", "Azure Table Storage",
       "Azure Files"],
      0,
      "Azure Data Factory orchestrates and schedules data movement and "
      "transformation pipelines for ingestion and processing.",
      "medium"),
]
