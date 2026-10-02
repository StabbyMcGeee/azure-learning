"""DP-900 launch-course items (fresh originals).

Authored from the public DP-900 skills outline ("Skills measured as of
July 21, 2026", retrieved 2026-10-02) and standard Microsoft Learn facts.
No legacy wording or recalled exam item was used.
"""

SRC = (
    "Original AI-fleet-authored content; publisher substantive review PENDING (Dimitri Meier); "
    "facts from Microsoft Learn DP-900 study guide (2026-07-21) and docs, "
    "retrieved 2026-10-02"
)
BASIS = "original-human-ai-assisted"
COURSE = "dp-900"


def q(id_, text, options, ci, expl, diff):
    return {
        "id": id_,
        "text": text,
        "options": options,
        "correctOptionIndex": ci,
        "explanation": expl,
        "domain": "Core Data Concepts",
        "difficulty": diff,
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    }


def qr(id_, text, options, ci, expl, diff):
    """Relational-data domain item."""
    d = q(id_, text, options, ci, expl, diff)
    d["domain"] = "Relational Data on Azure"
    return d


def qn(id_, text, options, ci, expl, diff):
    """Non-relational-data domain item."""
    d = q(id_, text, options, ci, expl, diff)
    d["domain"] = "Non-relational Data on Azure"
    return d


def qa(id_, text, options, ci, expl, diff):
    """Analytics-domain item."""
    d = q(id_, text, options, ci, expl, diff)
    d["domain"] = "Analytics Workload"
    return d


QUESTIONS = [
    # ---- Core data concepts ----
    q("dp-900-001",
      "Which type of data is organized into a fixed schema of rows and "
      "columns, such as a relational database table?",
      ["structured data", "unstructured data", "semi-structured data",
       "binary data"],
      0,
      "Structured data has a fixed schema and is organized into rows and "
      "columns, as in a relational database or spreadsheet.",
      "easy"),
    q("dp-900-002",
      "Which data format is an example of semi-structured data?",
      ["JSON", "A JPEG image", "An MP3 audio file", "A plain text log with no structure"],
      0,
      "JSON is semi-structured because it has some organization (key-value "
      "pairs) but no fixed relational schema. Images and audio are "
      "unstructured.",
      "easy"),
    q("dp-900-003",
      "Which type of data has no fixed schema or predefined structure?",
      ["unstructured data", "structured data", "semi-structured data",
       "tabular data"],
      0,
      "Unstructured data such as images, video, audio, and free-form text has "
      "no fixed schema.",
      "easy"),
    q("dp-900-004",
      "Which file format is columnar and optimized for large-scale analytical "
      "queries?",
      ["Parquet", "CSV", "JSON", "XML"],
      0,
      "Parquet is a columnar format that compresses and stores data by "
      "column, which makes it efficient for analytical queries.",
      "medium"),
    q("dp-900-005",
      "Which format is a simple, human-readable text format in which values "
      "are separated by commas?",
      ["CSV", "Parquet", "Avro", "ORC"],
      0,
      "CSV (comma-separated values) stores tabular data as plain text with "
      "values separated by commas.",
      "easy"),
    q("dp-900-006",
      "What is a database?",
      ["An organized collection of data stored and accessed electronically",
       "A physical server rack",
       "A network switch",
       "A programming language"],
      0,
      "A database is an organized collection of data that is stored and "
      "accessed electronically.",
      "easy"),
    q("dp-900-007",
      "A retailer stores catalog and order records that require strict "
      "consistency and relational queries. Which Azure datastore fits best?",
      ["Azure SQL Database", "Azure Blob Storage", "Azure Cosmos DB",
       "Azure Data Lake Storage"],
      0,
      "Azure SQL Database is a relational PaaS service suited to catalog and "
      "order records that need relational queries and consistency.",
      "medium"),
    q("dp-900-008",
      "Which workload is characterized by many small, fast read and write "
      "operations on current data, such as order entry?",
      ["A transactional workload", "An analytical workload", "A batch job",
       "An archive job"],
      0,
      "Transactional workloads (OLTP) process many small, fast point "
      "operations on current data, such as order entry.",
      "medium"),
    q("dp-900-009",
      "Which workload is characterized by large reads and aggregations over "
      "historical data to support reporting?",
      ["An analytical workload", "A transactional workload", "A backup job",
       "A data-entry job"],
      0,
      "Analytical workloads (OLAP) perform large reads and aggregations over "
      "historical data for reporting and analysis.",
      "medium"),
    q("dp-900-010",
      "Which role is primarily responsible for the availability, security, "
      "backups, and performance of databases?",
      ["A database administrator", "A data engineer", "A data analyst",
       "A software developer"],
      0,
      "A database administrator manages the availability, security, backups, "
      "and performance of databases.",
      "easy"),
    q("dp-900-011",
      "Which role builds and maintains the pipelines that ingest, transform, "
      "and move data between systems?",
      ["A data engineer", "A database administrator", "A data analyst",
       "A project manager"],
      0,
      "A data engineer builds and maintains data pipelines that ingest, "
      "transform, and move data between systems.",
      "easy"),
    q("dp-900-012",
      "Which role explores data, builds reports, and visualizes findings to "
      "answer business questions?",
      ["A data analyst", "A data engineer", "A database administrator",
       "A network administrator"],
      0,
      "A data analyst explores data, builds reports, and visualizes findings "
      "to answer business questions.",
      "easy"),
    # ---- Relational data on Azure ----
    qr("dp-900-013",
       "Which statement describes relational data?",
       ["Data is organized into tables with rows, columns, and relationships",
        "Data has no fixed schema",
        "Data is stored only as images",
        "Data cannot be queried with SQL"],
       0,
       "Relational data is organized into tables with rows and columns and "
       "uses keys to define relationships between tables.",
       "easy"),
    qr("dp-900-014",
       "What is the purpose of normalization in a relational database?",
       ["To reduce data redundancy and improve integrity",
        "To duplicate data across tables",
        "To store data as JSON",
        "To remove all tables"],
       0,
       "Normalization organizes data into related tables to reduce redundancy "
       "and improve data integrity.",
       "medium"),
    qr("dp-900-015",
       "In a normalized database, which key uniquely identifies a row in a "
       "table?",
       ["A primary key", "A foreign key", "A composite value", "An index"],
       0,
       "A primary key is the column or columns that uniquely identify each "
       "row in a table.",
       "medium"),
    qr("dp-900-016",
       "Which SQL statement retrieves rows from a table?",
       ["SELECT", "INSERT", "UPDATE", "DELETE"],
       0,
       "SELECT retrieves rows from a table. INSERT, UPDATE, and DELETE "
       "modify data.",
       "easy"),
    qr("dp-900-017",
       "Which SQL statement adds a new row to a table?",
       ["INSERT", "SELECT", "UPDATE", "DROP"],
       0,
       "INSERT adds a new row to a table.",
       "easy"),
    qr("dp-900-018",
       "Which database object is a virtual table defined by a saved query?",
       ["A view", "An index", "A stored procedure", "A primary key"],
       0,
       "A view is a virtual table defined by a saved query; it does not store "
       "data itself.",
       "medium"),
    qr("dp-900-019",
       "Which Azure SQL offering is a fully managed platform as a service "
       "(PaaS) relational database with automatic updates and backups?",
       ["Azure SQL Database", "SQL Server on Azure Virtual Machines",
        "Azure Blob Storage", "Azure Cosmos DB"],
       0,
       "Azure SQL Database is a fully managed PaaS relational database with "
       "automatic updates, backups, and high availability.",
       "medium"),
    qr("dp-900-020",
       "Which Azure SQL offering provides near-complete SQL Server "
       "compatibility in a managed PaaS instance, including cross-database "
       "queries?",
       ["Azure SQL Managed Instance", "Azure SQL Database",
        "SQL Server on Azure Virtual Machines", "Azure Table Storage"],
       0,
       "Azure SQL Managed Instance is a PaaS offering with near-complete SQL "
       "Server compatibility and features such as cross-database queries.",
       "medium"),
    qr("dp-900-021",
       "Which option gives you full control over the operating system and "
       "SQL Server installation in Azure?",
       ["SQL Server on Azure Virtual Machines", "Azure SQL Database",
        "Azure SQL Managed Instance", "Azure Database for MySQL"],
       0,
       "SQL Server on Azure Virtual Machines is an IaaS option that gives "
       "full control over the OS and SQL Server installation.",
       "medium"),
    qr("dp-900-022",
       "Which services are Azure PaaS offerings for open-source relational "
       "databases?",
       ["Azure Database for PostgreSQL and Azure Database for MySQL",
        "Azure Cosmos DB and Azure Blob Storage",
        "Azure Files and Azure Data Lake Storage",
        "Azure Databricks and Microsoft Fabric"],
       0,
       "Azure Database for PostgreSQL, Azure Database for MySQL, and Azure "
       "Database for MariaDB are managed PaaS open-source relational "
       "databases.",
       "medium"),
    # ---- Non-relational data on Azure ----
    qn("dp-900-023",
       "Which service is Azure's object store for unstructured data such as "
       "images, videos, and backups?",
       ["Azure Blob Storage", "Azure Files", "Azure Table Storage",
        "Azure SQL Database"],
       0,
       "Azure Blob Storage is object storage for unstructured data such as "
       "images, videos, and backups.",
       "easy"),
    qn("dp-900-024",
       "Which type of Azure Blob is optimized for text and binary data such "
       "as documents and media?",
       ["Block blobs", "Append blobs", "Page blobs", "Queue blobs"],
       0,
       "Block blobs store text and binary data such as documents and media. "
       "Append blobs suit logs, and page blobs suit virtual disks.",
       "medium"),
    qn("dp-900-025",
       "Which service provides fully managed file shares that can be mounted "
       "over SMB or NFS?",
       ["Azure Files", "Azure Blob Storage", "Azure Table Storage",
        "Azure Cosmos DB"],
       0,
       "Azure Files provides fully managed file shares mountable over SMB or "
       "NFS.",
       "easy"),
    qn("dp-900-026",
       "Which service is a NoSQL key-value store for semi-structured data "
       "with fast lookups?",
       ["Azure Table Storage", "Azure Files", "Azure Blob Storage",
        "Azure SQL Database"],
       0,
       "Azure Table Storage is a NoSQL key-value store for semi-structured "
       "data with fast, inexpensive lookups.",
       "medium"),
    qn("dp-900-027",
       "Which service is a globally distributed, multi-model NoSQL database "
       "with low-latency access at any scale?",
       ["Azure Cosmos DB", "Azure Table Storage", "Azure SQL Database",
        "Azure Blob Storage"],
       0,
       "Azure Cosmos DB is a globally distributed, multi-model NoSQL database "
       "designed for low-latency access at scale.",
       "medium"),
    qn("dp-900-028",
       "Which workload is a good fit for Azure Cosmos DB?",
       ["A globally distributed application needing low-latency data access",
        "A strictly relational order-entry system with no global reach",
        "Bulk image backup storage",
        "Mountable file shares for a lift-and-shift VM"],
       0,
       "Azure Cosmos DB suits globally distributed applications that need "
       "low-latency access to data across regions.",
       "medium"),
    qn("dp-900-029",
       "Which Azure Cosmos DB API uses SQL-like syntax for document data?",
       ["Core (SQL) API", "MongoDB API", "Gremlin API", "Table API"],
       0,
       "The Core (SQL) API stores documents and queries them with SQL-like "
       "syntax.",
       "medium"),
    qn("dp-900-030",
       "Which Azure Cosmos DB API is designed for graph data and traversals?",
       ["Gremlin API", "Core (SQL) API", "Table API", "Cassandra API"],
       0,
       "The Gremlin API stores graph data (entities and relationships) and "
       "supports graph traversals.",
       "medium"),
    # ---- Analytics workload ----
    qa("dp-900-031",
       "What is data ingestion?",
       ["The process of loading data from sources into a storage or processing system",
        "The process of deleting old data",
        "The process of encrypting data at rest",
        "The process of visualizing data"],
       0,
       "Data ingestion loads data from source systems into a storage or "
       "processing system, either in batches or as a stream.",
       "medium"),
    qa("dp-900-032",
       "Which transformation order describes extract, transform, load?",
       ["Transform data after extraction and before loading into the target",
        "Load raw data first and transform it later",
        "Delete data before loading",
        "Visualize data before extraction"],
       0,
       "ETL (extract, transform, load) transforms data after extraction and "
       "before loading it into the target store.",
       "medium"),
    qa("dp-900-033",
       "Which analytical data store is optimized for structured, relational "
       "data and fast aggregations for reporting?",
       ["A data warehouse", "A data lake", "An object store", "A key-value store"],
       0,
       "A data warehouse stores structured, relational data optimized for "
       "fast aggregations and reporting.",
       "medium"),
    qa("dp-900-034",
       "Which analytical data store holds large volumes of raw data in its "
       "native format at low cost?",
       ["A data lake", "A data warehouse", "A transactional database",
        "A file share"],
       0,
       "A data lake stores large volumes of raw, structured and unstructured "
       "data in its native format at low cost.",
       "medium"),
    qa("dp-900-035",
       "Which service is an Apache Spark-based analytics platform for "
       "large-scale data processing?",
       ["Azure Databricks", "Microsoft Power BI", "Azure Table Storage",
        "Azure Files"],
       0,
       "Azure Databricks is an Apache Spark-based analytics platform for "
       "large-scale data processing and machine learning.",
       "medium"),
    qa("dp-900-036",
       "Which service is a unified software as a service (SaaS) analytics "
       "platform that combines data engineering, warehousing, and business "
       "intelligence?",
       ["Microsoft Fabric", "Azure Databricks", "Azure Blob Storage",
        "Azure Cosmos DB"],
       0,
       "Microsoft Fabric is a unified SaaS analytics platform that combines "
       "data engineering, warehousing, real-time analytics, and Power BI.",
       "medium"),
    qa("dp-900-037",
       "Which term describes processing data as it arrives, with near "
       "real-time latency?",
       ["Streaming data", "Batch data", "Archived data", "Structured data"],
       0,
       "Streaming data is processed as events arrive, enabling near "
       "real-time latency, unlike batch processing on a schedule.",
       "easy"),
    qa("dp-900-038",
       "Which term describes processing large volumes of data on a schedule, "
       "such as nightly?",
       ["Batch data", "Streaming data", "Real-time data", "Event data"],
       0,
       "Batch data is processed in large volumes on a schedule, with latency "
       "of minutes to hours rather than seconds.",
       "easy"),
    qa("dp-900-039",
       "Which service queries streaming data from sources such as Azure Event "
       "Hubs in real time?",
       ["Azure Stream Analytics", "Azure Cosmos DB", "Azure SQL Database",
        "Azure Files"],
       0,
       "Azure Stream Analytics processes and queries streaming data from "
       "sources such as Azure Event Hubs in real time.",
       "medium"),
    qa("dp-900-040",
       "Which service provides fast exploration and analysis of large "
       "volumes of log and telemetry data?",
       ["Azure Data Explorer", "Azure Blob Storage", "Azure Table Storage",
        "Azure SQL Database"],
       0,
       "Azure Data Explorer provides fast, interactive analysis of large "
       "volumes of log and telemetry data.",
       "medium"),
    qa("dp-900-041",
       "Which tool is Microsoft's business intelligence service for creating "
       "reports and dashboards?",
       ["Microsoft Power BI", "Azure Databricks", "Azure Data Explorer",
        "Azure Stream Analytics"],
       0,
       "Microsoft Power BI is Microsoft's business intelligence service for "
       "creating reports, dashboards, and visualizations.",
       "easy"),
    qa("dp-900-042",
       "Which capability lets Power BI connect to many sources and combine "
       "them for analysis?",
       ["Data connectivity and transformation",
        "Physical storage of server racks",
        "Relational database normalization",
        "Graph traversal"],
       0,
       "Power BI connects to many data sources and transforms the data "
       "during import for analysis.",
       "medium"),
    qa("dp-900-043",
       "In a Power BI data model, what defines how two tables are related?",
       ["A relationship between tables",
        "A primary color",
        "A file extension",
        "A network subnet"],
       0,
       "A Power BI data model defines relationships between tables so fields "
       "can be combined across them in reports.",
       "medium"),
    qa("dp-900-044",
       "Which language is used to define calculated measures in a Power BI "
       "data model?",
       ["DAX", "SQL", "Python", "HTML"],
       0,
       "DAX (Data Analysis Expressions) defines calculated measures and "
       "columns in Power BI data models.",
       "medium"),
    qa("dp-900-045",
       "Which Power BI element is best for showing geographic data on a map?",
       ["A map visualization", "A bar chart", "A table", "A slicer"],
       0,
       "A map visualization displays geographic data using location fields "
       "such as country or latitude and longitude.",
       "medium"),
    qa("dp-900-046",
       "Which Power BI element filters a report interactively by selecting "
       "values such as a year or region?",
       ["A slicer", "A map", "A pie chart", "A line chart"],
       0,
       "A slicer is an interactive filter that lets a report viewer select "
       "values such as year or region.",
       "medium"),
]
