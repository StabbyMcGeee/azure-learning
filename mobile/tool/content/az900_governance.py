"""AZ-900 management-and-governance replacement items (fresh originals).

Covers the 52 governance-category legacy slots. Items whose public objective is
an architecture-and-services topic (Azure RBAC, Microsoft Defender for Cloud,
sovereign regions) carry that domain tag. Legacy wording was not read or reused.
"""

SRC = (
    "Original AI-fleet-authored content with publisher review (Dimitri Meier); "
    "facts from Microsoft Learn, retrieved 2026-10-02"
)
BASIS = "original-human-ai-assisted"
COURSE = "az-900"

MG = "Azure Management and Governance"
AA = "Azure Architecture and Services"


def q(id_, text, options, ci, expl, diff, domain=MG):
    return {
        "id": id_,
        "text": text,
        "options": options,
        "correctOptionIndex": ci,
        "explanation": expl,
        "domain": domain,
        "difficulty": diff,
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    }


QUESTIONS = [
    # az-900-023 -> MG.1 Azure pricing calculator
    q("az-900-023",
      "Which tool estimates the cost of Azure resources before you deploy "
      "them?",
      [
          "Azure pricing calculator",
          "Microsoft Cost Management",
          "Azure Advisor",
          "Azure Service Health",
      ],
      0,
      "The Azure pricing calculator estimates the cost of Azure resources "
      "before deployment based on selected services and configurations.",
      "easy"),
    # az-900-024 -> MG.1 tags
    q("az-900-024",
      "Which Azure feature applies name-value pairs to resources to help "
      "organize and track them?",
      [
          "tags",
          "resource locks",
          "Azure Policy",
          "management groups",
      ],
      0,
      "Tags are name-value pairs applied to resources to organize them and "
      "track attributes such as cost center or environment.",
      "easy"),
    # az-900-025 -> MG.2 resource locks
    q("az-900-025",
      "Which feature prevents a resource from being accidentally deleted or "
      "modified?",
      [
          "resource locks",
          "Azure Policy",
          "tags",
          "Azure Advisor",
      ],
      0,
      "Resource locks prevent accidental deletion or modification of "
      "resources by applying a read-only or delete lock.",
      "medium"),
    # az-900-026 -> MG.2 Azure Policy
    q("az-900-026",
      "Which service enforces rules and standards for Azure resources, such "
      "as restricting which regions or virtual machine sizes are allowed?",
      [
          "Azure Policy",
          "Azure Advisor",
          "Azure Monitor",
          "Azure Service Health",
      ],
      0,
      "Azure Policy enforces organizational rules and standards for "
      "resources, such as allowed regions and virtual machine sizes.",
      "medium"),
    # az-900-027 -> MG.4 Azure Advisor (defect item, fresh original)
    q("az-900-027",
      "Which service provides personalized recommendations for reliability, "
      "security, cost, operational excellence, and performance?",
      [
          "Azure Advisor",
          "Azure Monitor",
          "Azure Service Health",
          "Microsoft Purview",
      ],
      0,
      "Azure Advisor provides personalized recommendations across "
      "reliability, security, cost, operational excellence, and performance.",
      "medium"),
    # az-900-028 -> MG.3 Azure Cloud Shell
    q("az-900-028",
      "Which feature provides a browser-based command-line environment for "
      "managing Azure resources?",
      [
          "Azure Cloud Shell",
          "Azure portal",
          "Azure Arc",
          "Azure Policy",
      ],
      0,
      "Azure Cloud Shell is a browser-based command-line environment with "
      "Azure CLI and Azure PowerShell for managing resources.",
      "easy"),
    # az-900-029 -> MG.3 Azure Resource Manager (ARM)
    q("az-900-029",
      "What is the role of Azure Resource Manager (ARM)?",
      [
          "The deployment and management service for Azure resources",
          "A storage redundancy option",
          "A monitoring dashboard",
          "A billing currency setting",
      ],
      0,
      "Azure Resource Manager (ARM) is the deployment and management "
      "service for Azure, handling resource creation, updates, and deletion.",
      "medium"),
    # az-900-030 -> MG.3 ARM templates
    q("az-900-030",
      "What is an ARM template?",
      [
          "A declarative JSON file that defines Azure resources for deployment",
          "A PowerShell script for logging in",
          "A cost report",
          "A virtual machine image",
      ],
      0,
      "An ARM template is a declarative JSON file that defines the Azure "
      "resources and configuration to deploy.",
      "medium"),
    # az-900-031 -> MG.4 Azure Monitor Application Insights
    q("az-900-031",
      "Which service monitors a live application's performance, failures, "
      "and usage?",
      [
          "Azure Monitor Application Insights",
          "Azure Service Health",
          "Azure Advisor",
          "Azure Policy",
      ],
      0,
      "Azure Monitor Application Insights monitors live application "
      "performance, failures, and usage telemetry.",
      "medium"),
    # az-900-032 -> MG.2 Azure Policy
    q("az-900-032",
      "Which statement about Azure Policy is correct?",
      [
          "It evaluates resources for compliance with defined rules",
          "It provides cost recommendations",
          "It monitors application performance",
          "It manages virtual network peering",
      ],
      0,
      "Azure Policy evaluates resources against defined rules and reports "
      "compliance, helping enforce standards at scale.",
      "hard"),
    # az-900-033 -> MG.3 Azure Arc
    q("az-900-033",
      "Which service extends Azure management to servers and Kubernetes "
      "clusters running outside Azure?",
      [
          "Azure Arc",
          "Azure Cloud Shell",
          "Azure Advisor",
          "Azure Service Health",
      ],
      0,
      "Azure Arc extends Azure management and governance to resources "
      "running on-premises or in other clouds.",
      "medium"),
    # az-900-034 -> MG.1 Microsoft Cost Management
    q("az-900-034",
      "Which service provides cost analysis, budgets, and recommendations to "
      "control cloud spending?",
      [
          "Microsoft Cost Management",
          "Azure Advisor",
          "Azure Monitor",
          "Azure Policy",
      ],
      0,
      "Microsoft Cost Management provides cost analysis, budgets, and "
      "recommendations to monitor and control cloud spending.",
      "easy"),
    # az-900-035 -> MG.4 Azure Monitor alerts
    q("az-900-035",
      "Which capability notifies you when a metric or log condition is met, "
      "such as high CPU usage?",
      [
          "Azure Monitor alerts",
          "Azure Policy",
          "resource locks",
          "tags",
      ],
      0,
      "Azure Monitor alerts notify you when a monitored metric or log "
      "condition is met.",
      "medium"),
    # az-900-036 -> MG.3 infrastructure as code / ARM templates (defect, fresh)
    q("az-900-036",
      "Which practice defines and deploys infrastructure using declarative "
      "files rather than manual portal steps?",
      [
          "infrastructure as code (IaC)",
          "Azure Advisor",
          "Azure Service Health",
          "Microsoft Purview",
      ],
      0,
      "Infrastructure as code (IaC) defines and deploys infrastructure using "
      "declarative files such as ARM templates rather than manual steps.",
      "medium"),
    # az-900-037 -> MG.4 Azure Advisor
    q("az-900-037",
      "Which service should you review first for suggestions on reducing "
      "wasted cloud spend?",
      [
          "Azure Advisor",
          "Azure Monitor alerts",
          "Azure Service Health",
          "Azure Policy",
      ],
      0,
      "Azure Advisor provides cost recommendations, including suggestions "
      "for reducing wasted spend.",
      "easy"),
    # az-900-038 -> MG.4 Azure Service Health
    q("az-900-038",
      "Which service reports service issues, planned maintenance, and health "
      "advisories affecting your Azure resources?",
      [
          "Azure Service Health",
          "Azure Advisor",
          "Azure Monitor",
          "Azure Policy",
      ],
      0,
      "Azure Service Health reports service issues, planned maintenance, and "
      "health advisories affecting your resources.",
      "medium"),
    # az-900-039 -> AA.4 Azure role-based access control (Azure RBAC)
    q("az-900-039",
      "Which service grants permissions to Azure resources using roles such "
      "as Owner, Contributor, and Reader?",
      [
          "Azure role-based access control (RBAC)",
          "Azure Policy",
          "Azure Advisor",
          "Microsoft Purview",
      ],
      0,
      "Azure role-based access control (RBAC) grants permissions to "
      "resources using built-in or custom roles such as Owner, Contributor, "
      "and Reader.",
      "easy",
      AA),
    # az-900-040 -> MG.4 Azure Monitor
    q("az-900-040",
      "Which service collects and analyzes metrics and logs from Azure and "
      "on-premises resources?",
      [
          "Azure Monitor",
          "Azure Advisor",
          "Azure Service Health",
          "Azure Policy",
      ],
      0,
      "Azure Monitor collects and analyzes metrics and logs from Azure and "
      "on-premises resources.",
      "easy"),
    # az-900-044 -> MG.2 Azure Policy / resource locks / tags (defect, fresh)
    q("az-900-044",
      "Which combination best enforces governance on a resource group?",
      [
          "Azure Policy, resource locks, and tags",
          "Azure Advisor and Azure Service Health",
          "Azure Monitor and Log Analytics",
          "AzCopy and Azure Storage Explorer",
      ],
      0,
      "Azure Policy enforces rules, resource locks prevent unwanted changes, "
      "and tags organize resources; together they enforce governance.",
      "medium"),
    # az-900-050 -> MG.3 ARM templates
    q("az-900-050",
      "What is a benefit of using ARM templates for deployment?",
      [
          "Repeatable, consistent, and declarative deployments",
          "They guarantee the lowest cost",
          "They replace the need for identity management",
          "They automatically patch operating systems",
      ],
      0,
      "ARM templates provide repeatable, consistent, and declarative "
      "deployments of Azure resources.",
      "medium"),
    # az-900-051 -> MG.4 Log Analytics
    q("az-900-051",
      "Which service lets you query collected log data using a query language "
      "to investigate issues?",
      [
          "Log Analytics",
          "Azure Advisor",
          "Azure Service Health",
          "Azure Policy",
      ],
      0,
      "Log Analytics is a tool in Azure Monitor for querying and analyzing "
      "collected log data.",
      "medium"),
    # az-900-057 -> MG.2 Microsoft Purview
    q("az-900-057",
      "Which service helps an organization govern, protect, and manage its "
      "data across on-premises and cloud environments?",
      [
          "Microsoft Purview",
          "Azure Advisor",
          "Azure Monitor",
          "Azure Arc",
      ],
      0,
      "Microsoft Purview provides data governance, protection, and "
      "management across on-premises and cloud environments.",
      "medium"),
    # az-900-058 -> AA.4 Microsoft Defender for Cloud
    q("az-900-058",
      "Which service provides cloud security posture management and workload "
      "protection across Azure and hybrid environments?",
      [
          "Microsoft Defender for Cloud",
          "Azure Policy",
          "Azure Advisor",
          "Azure Service Health",
      ],
      0,
      "Microsoft Defender for Cloud provides cloud security posture "
      "management and workload protection across Azure and hybrid environments.",
      "medium",
      AA),
    # az-900-059 -> MG.3 Azure Cloud Shell
    q("az-900-059",
      "Which pair of command-line tools are available inside Azure Cloud Shell?",
      [
          "Azure CLI and Azure PowerShell",
          "AzCopy and Azure Storage Explorer",
          "ARM templates and Bicep",
          "Azure Advisor and Azure Monitor",
      ],
      0,
      "Azure Cloud Shell provides Azure CLI and Azure PowerShell for "
      "managing Azure resources from a browser.",
      "medium"),
    # az-900-060 -> MG.4 Azure Service Health (Azure Resource Health)
    q("az-900-060",
      "Which part of Azure Service Health reports the health of a specific "
      "individual resource?",
      [
          "Azure Resource Health",
          "Azure Advisor",
          "Log Analytics",
          "Azure Policy",
      ],
      0,
      "Azure Resource Health, part of Azure Service Health, reports the "
      "health of an individual resource.",
      "medium"),
    # az-900-062 -> MG.3 ARM templates
    q("az-900-062",
      "Which language format are ARM templates written in?",
      [
          "JSON",
          "PowerShell",
          "C#",
          "SQL",
      ],
      0,
      "ARM templates are declarative JSON files that describe Azure "
      "resources and their configuration.",
      "hard"),
    # az-900-064 -> MG.4 Azure Monitor alerts
    q("az-900-064",
      "Which action best uses Azure Monitor alerts?",
      [
          "Sending a notification when a metric threshold is crossed",
          "Enforcing naming conventions on resources",
          "Estimating deployment costs",
          "Storing unstructured blob data",
      ],
      0,
      "Azure Monitor alerts send notifications or trigger actions when a "
      "metric or log threshold is crossed.",
      "hard"),
    # az-900-066 -> MG.4 Azure Advisor
    q("az-900-066",
      "Which category of Azure Advisor recommendations helps improve the "
      "reliability of a workload?",
      [
          "Reliability recommendations",
          "Cost recommendations",
          "Security recommendations",
          "Operational excellence recommendations",
      ],
      0,
      "Azure Advisor groups recommendations into categories including "
      "reliability, security, cost, operational excellence, and performance.",
      "easy"),
    # az-900-073 -> MG.2 resource locks
    q("az-900-073",
      "Which resource lock type prevents both deletion and modification of a "
      "resource?",
      [
          "A read-only lock",
          "A delete lock",
          "A tag",
          "A policy assignment",
      ],
      0,
      "A read-only lock prevents both deletion and modification; a delete "
      "lock prevents only deletion.",
      "hard"),
    # az-900-074 -> MG.1 Microsoft Cost Management (Cost analysis)
    q("az-900-074",
      "Which Microsoft Cost Management feature helps you view and break down "
      "spending by resource, service, or tag?",
      [
          "Cost analysis",
          "Budgets",
          "The pricing calculator",
          "Reservations",
      ],
      0,
      "Cost analysis in Microsoft Cost Management lets you view and break "
      "down spending by resource, service, or tag.",
      "hard"),
    # az-900-075 -> MG.2 Azure Policy
    q("az-900-075",
      "A team must ensure no storage account allows public blob access. Which "
      "service enforces this automatically?",
      [
          "Azure Policy",
          "Azure Advisor",
          "Azure Service Health",
          "Azure Monitor",
      ],
      0,
      "Azure Policy can enforce a rule that storage accounts deny public "
      "blob access and report non-compliance.",
      "hard"),
    # az-900-076 -> MG.2 Azure Policy
    q("az-900-076",
      "A subscription must reject any resource that violates a compliance "
      "rule before it is created. Which Azure Policy capability achieves "
      "this?",
      [
          "It can prevent non-compliant resources from being created",
          "It provides personalized cost-saving advice",
          "It monitors application latency",
          "It manages user passwords",
      ],
      0,
      "Azure Policy can deny the creation of non-compliant resources or "
      "report them as non-compliant.",
      "medium"),
    # az-900-082 -> AA.4 Azure role-based access control (Azure RBAC)
    q("az-900-082",
      "Which principle does Azure role-based access control (RBAC) follow "
      "when granting access?",
      [
          "Grant users the least privilege needed to do their job",
          "Give every user the Owner role",
          "Share one administrator password",
          "Disable all access by default with no way to grant it",
      ],
      0,
      "Azure role-based access control (RBAC) follows least privilege: users "
      "receive only the roles and permissions they need.",
      "hard",
      AA),
    # az-900-083 -> MG.2 Azure Policy
    q("az-900-083",
      "Which Azure Policy effect prevents a non-compliant resource from being "
      "created at all?",
      [
          "Deny",
          "Audit",
          "Append",
          "DeployIfNotExists",
      ],
      0,
      "The Deny effect in Azure Policy blocks creation or modification of "
      "non-compliant resources.",
      "medium"),
    # az-900-084 -> MG.4 Azure Service Health
    q("az-900-084",
      "Which source tells you about a regional Azure outage affecting many "
      "customers?",
      [
          "Azure Service Health",
          "Azure Advisor",
          "Log Analytics",
          "Azure Policy",
      ],
      0,
      "Azure Service Health reports service issues and regional outages "
      "affecting Azure services and your resources.",
      "medium"),
    # az-900-094 -> MG.2 Azure Policy
    q("az-900-094",
      "What is an initiative in Azure Policy?",
      [
          "A group of related policy definitions applied together",
          "A single virtual machine",
          "A cost-saving recommendation",
          "A monitoring alert rule",
      ],
      0,
      "An initiative groups related policy definitions so they can be "
      "assigned and managed together.",
      "hard"),
    # az-900-095 -> MG.1 Microsoft Cost Management (budgets)
    q("az-900-095",
      "Which Microsoft Cost Management feature alerts you when spending "
      "approaches a limit you set?",
      [
          "Budgets",
          "Cost analysis",
          "The pricing calculator",
          "Tags",
      ],
      0,
      "Budgets in Microsoft Cost Management let you set spending limits and "
      "receive alerts when spending approaches them.",
      "hard"),
    # az-900-096 -> MG.2 Azure Policy
    q("az-900-096",
      "Which component attaches an Azure Policy definition to a specific "
      "scope such as a subscription or resource group?",
      [
          "A policy assignment",
          "A resource lock",
          "A tag",
          "A role assignment",
      ],
      0,
      "A policy assignment applies a policy definition to a scope such as a "
      "management group, subscription, or resource group.",
      "hard"),
    # az-900-103 -> MG.3 Bicep / IaC (adjacent)
    q("az-900-103",
      "Which practice describes defining infrastructure in code files that "
      "can be versioned and redeployed consistently?",
      [
          "infrastructure as code (IaC)",
          "Azure Service Health",
          "Azure Advisor",
          "Microsoft Purview",
      ],
      0,
      "Infrastructure as code (IaC) defines infrastructure in versioned code "
      "files for consistent, repeatable deployment.",
      "hard"),
    # az-900-104 -> MG.4 Azure Advisor
    q("az-900-104",
      "Which Azure Advisor category recommends resizing or shutting down "
      "underused resources to save money?",
      [
          "Cost",
          "Reliability",
          "Security",
          "Performance",
      ],
      0,
      "Azure Advisor cost recommendations suggest resizing or shutting down "
      "underused resources to reduce spend.",
      "medium"),
    # az-900-105 -> MG.4 Log Analytics
    q("az-900-105",
      "Which tool stores and queries log data collected by Azure Monitor?",
      [
          "Log Analytics",
          "Azure Advisor",
          "Azure Service Health",
          "Azure Policy",
      ],
      0,
      "Log Analytics stores and queries log data collected by Azure Monitor.",
      "hard"),
    # az-900-106 -> MG.4 Azure Monitor
    q("az-900-106",
      "Which service would you use to gain a unified view of metrics and logs "
      "across your Azure resources?",
      [
          "Azure Monitor",
          "Azure Advisor",
          "Azure Policy",
          "Azure Service Health",
      ],
      0,
      "Azure Monitor provides a unified view of metrics and logs across "
      "Azure resources.",
      "hard"),
    # az-900-112 -> MG.4 Azure Monitor
    q("az-900-112",
      "Which statement about Azure Monitor is correct?",
      [
          "It collects metrics and logs for analysis and alerting",
          "It enforces resource naming rules",
          "It estimates deployment costs",
          "It manages storage redundancy",
      ],
      0,
      "Azure Monitor collects metrics and logs from Azure resources for "
      "analysis, visualization, and alerting.",
      "hard"),
    # az-900-113 -> AA.4 Azure role-based access control (Azure RBAC)
    q("az-900-113",
      "Which role typically has full management access to a resource group "
      "but cannot grant access to others?",
      [
          "Contributor",
          "Reader",
          "Owner",
          "User Access Administrator",
      ],
      0,
      "Contributor can create and manage resources but cannot grant access; "
      "granting access requires Owner or User Access Administrator.",
      "hard",
      AA),
    # az-900-114 -> MG.2 Azure Policy
    q("az-900-114",
      "A policy requires all virtual machines to use a specific image. Which "
      "effect reports existing non-compliant VMs without blocking them?",
      [
          "Audit",
          "Deny",
          "Delete",
          "Lock",
      ],
      0,
      "The Audit effect reports non-compliant resources without blocking "
      "them, unlike Deny which blocks creation.",
      "hard"),
    # az-900-115 -> MG.4 Azure Service Health (Azure Resource Health)
    q("az-900-115",
      "Which signal would Azure Resource Health report about a virtual "
      "machine?",
      [
          "Whether the resource is available and healthy",
          "The monthly cost of the resource",
          "The tags applied to the resource",
          "The resource's role assignments",
      ],
      0,
      "Azure Resource Health reports whether an individual resource is "
      "available and healthy.",
      "hard"),
    # az-900-124 -> MG.1 Azure Hybrid Benefit
    q("az-900-124",
      "Which benefit lets you use existing on-premises licenses to reduce "
      "the cost of running certain workloads in Azure?",
      [
          "Azure Hybrid Benefit",
          "Azure Reservations",
          "Azure Spot Virtual Machines",
          "The pricing calculator",
      ],
      0,
      "Azure Hybrid Benefit lets you use existing on-premises licenses to "
      "reduce the cost of eligible Azure workloads.",
      "medium"),
    # az-900-125 -> MG.1 Microsoft Cost Management (re-scoped from support plans)
    q("az-900-125",
      "Which service helps you monitor spending, set budgets, and receive "
      "alerts when costs exceed thresholds?",
      [
          "Microsoft Cost Management",
          "Azure Advisor",
          "Azure Service Health",
          "Azure Monitor",
      ],
      0,
      "Microsoft Cost Management helps monitor spending, set budgets, and "
      "alert when costs exceed thresholds.",
      "medium"),
    # az-900-126 -> MG.2 Microsoft Purview (re-scoped from compliance offerings)
    q("az-900-126",
      "Which service helps an organization discover, classify, and govern "
      "sensitive data across its estate?",
      [
          "Microsoft Purview",
          "Azure Advisor",
          "Azure Monitor",
          "Azure Service Health",
      ],
      0,
      "Microsoft Purview discovers, classifies, and governs data across an "
      "organization's on-premises and cloud estate.",
      "medium"),
    # az-900-130 -> AA.1 sovereign regions (adjacent: EU Data Boundary)
    q("az-900-130",
      "Which type of region provides isolated Azure environments for "
      "customers with strict legal or compliance requirements?",
      [
          "sovereign regions",
          "region pairs",
          "availability zones",
          "public regions",
      ],
      0,
      "Sovereign regions are isolated Azure environments for customers with "
      "strict legal or compliance requirements.",
      "medium",
      AA),
    # az-900-131 -> MG.3 Azure Arc
    q("az-900-131",
      "Which service lets you manage on-premises servers using Azure "
      "governance tools such as Azure Policy?",
      [
          "Azure Arc",
          "Azure Cloud Shell",
          "Azure Advisor",
          "Azure Monitor alerts",
      ],
      0,
      "Azure Arc extends Azure management and governance, including Azure "
      "Policy, to on-premises and multi-cloud resources.",
      "medium"),
    # az-900-132 -> MG.3 Azure Arc (re-scoped from Azure Lighthouse)
    q("az-900-132",
      "Which service provides a unified way to govern and manage resources "
      "across on-premises and other clouds?",
      [
          "Azure Arc",
          "Azure Cloud Shell",
          "Azure Advisor",
          "Azure Service Health",
      ],
      0,
      "Azure Arc provides unified management and governance across "
      "on-premises, multi-cloud, and edge resources.",
      "medium"),
]
