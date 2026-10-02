"""AZ-900 architecture-and-services replacement items (fresh originals).

Covers the 49 architecture-category legacy slots plus the 7 outline topics the
legacy bank never covered (Azure Virtual Desktop, sovereign regions, Microsoft
Entra Domain Services, external identities, AzCopy, Azure File Sync, Azure
Storage Explorer). Legacy wording was not read or reused.
"""

SRC = (
    "Original AI-fleet-authored content with publisher review (Dimitri Meier); "
    "facts from Microsoft Learn, retrieved 2026-10-02"
)
BASIS = "original-human-ai-assisted"
COURSE = "az-900"


def q(id_, text, options, ci, expl, diff):
    return {
        "id": id_,
        "text": text,
        "options": options,
        "correctOptionIndex": ci,
        "explanation": expl,
        "domain": "Azure Architecture and Services",
        "difficulty": diff,
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    }


QUESTIONS = [
    # az-900-009 -> AA.1 resources / resource groups
    q("az-900-009",
      "What is the purpose of an Azure resource group?",
      [
          "To act as a logical container for related Azure resources",
          "To provide a physical building for datacenter servers",
          "To define billing currency for a subscription",
          "To store user passwords",
      ],
      0,
      "A resource group is a logical container that holds related Azure "
      "resources so they can be managed, secured, and deleted together.",
      "easy"),
    # az-900-010 -> AA.1 availability zones
    q("az-900-010",
      "What is an availability zone in Azure?",
      [
          "A physically separate datacenter within an Azure region",
          "A logical partition of a subscription",
          "A geographic area that contains two or more regions",
          "A network security boundary",
      ],
      0,
      "An availability zone is a physically separate datacenter within an "
      "Azure region, providing fault isolation and high availability.",
      "medium"),
    # az-900-011 -> AA.2 compute types
    q("az-900-011",
      "Which compute option gives you full control over the operating system "
      "and installed software?",
      [
          "virtual machines",
          "functions",
          "serverless apps",
          "containers on a managed platform",
      ],
      0,
      "Azure Virtual Machines are an infrastructure as a service (IaaS) "
      "option that gives full control over the operating system and "
      "installed software.",
      "medium"),
    # az-900-012 -> AA.2 virtual networks / subnets / peering
    q("az-900-012",
      "A network engineer needs to connect two Azure virtual networks so "
      "their resources can communicate privately. Which feature does this?",
      [
          "virtual network peering",
          "a public endpoint",
          "a storage account",
          "an availability set",
      ],
      0,
      "Virtual network peering connects two Azure virtual networks so "
      "resources can communicate privately using the Azure backbone.",
      "medium"),
    # az-900-013 -> AA.2 Azure ExpressRoute
    q("az-900-013",
      "Which service provides a private connection between an on-premises "
      "network and Azure that does not travel over the public internet?",
      [
          "Azure ExpressRoute",
          "Azure VPN Gateway",
          "Azure DNS",
          "Azure Front Door",
      ],
      0,
      "Azure ExpressRoute provides a private, dedicated connection between "
      "an on-premises network and Azure, avoiding the public internet.",
      "medium"),
    # az-900-014 -> AA.3 Azure Blob Storage
    q("az-900-014",
      "Which storage service is designed for unstructured data such as "
      "images, videos, and log files stored as objects?",
      [
          "Azure Blob Storage",
          "Azure Files",
          "Azure Queue Storage",
          "Azure Table Storage",
      ],
      0,
      "Azure Blob Storage is object storage for unstructured data such as "
      "images, videos, documents, and logs.",
      "easy"),
    # az-900-015 -> AA.3 redundancy options
    q("az-900-015",
      "Which redundancy option replicates data synchronously across three "
      "availability zones within the primary region?",
      [
          "zone-redundant storage (ZRS)",
          "locally redundant storage (LRS)",
          "geo-redundant storage (GRS)",
          "geo-zone-redundant storage (GZRS)",
      ],
      0,
      "Zone-redundant storage (ZRS) replicates data synchronously across "
      "three availability zones in the primary region.",
      "medium"),
    # az-900-016 -> AA.4 Microsoft Entra Conditional Access
    q("az-900-016",
      "Which feature applies policies that allow or block access to "
      "resources based on signals such as user, device, and location?",
      [
          "Microsoft Entra Conditional Access",
          "Azure role-based access control (RBAC)",
          "Azure Policy",
          "resource locks",
      ],
      0,
      "Microsoft Entra Conditional Access evaluates signals such as user, "
      "device, and location and applies policies that allow or block access.",
      "medium"),
    # az-900-017 -> AA.4 Zero Trust
    q("az-900-017",
      "Which security model assumes that no user, device, or network is "
      "trusted by default and requires explicit verification?",
      [
          "Zero Trust",
          "defense-in-depth",
          "shared responsibility model",
          "least-cost routing",
      ],
      0,
      "Zero Trust is a security model that verifies every request explicitly "
      "and assumes breach, rather than trusting a network boundary.",
      "medium"),
    # az-900-018 -> AA.2 Azure Virtual Machine Scale Sets
    q("az-900-018",
      "Which service deploys and manages a group of identical virtual "
      "machines and can automatically increase or decrease their number?",
      [
          "Azure Virtual Machine Scale Sets",
          "Azure Virtual Desktop",
          "Azure App Service",
          "Azure Functions",
      ],
      0,
      "Azure Virtual Machine Scale Sets deploy and manage identical VMs and "
      "can scale the number of instances in or out automatically.",
      "medium"),
    # az-900-020 -> AA.1 management groups
    q("az-900-020",
      "What is the purpose of Azure management groups?",
      [
          "To organize subscriptions and apply governance at scale",
          "To group virtual machines for load balancing",
          "To store billing invoices",
          "To connect on-premises networks",
      ],
      0,
      "Management groups organize subscriptions into a hierarchy and let you "
      "apply governance such as Azure Policy at scale.",
      "medium"),
    # az-900-021 -> AA.3 Azure Migrate
    q("az-900-021",
      "Which service provides tools to discover, assess, and migrate "
      "on-premises servers and databases to Azure?",
      [
          "Azure Migrate",
          "Azure Data Box",
          "Azure File Sync",
          "AzCopy",
      ],
      0,
      "Azure Migrate is a hub of tools for discovering, assessing, and "
      "migrating on-premises servers, databases, and apps to Azure.",
      "medium"),
    # az-900-022 -> AA.4 Microsoft Entra ID
    q("az-900-022",
      "Which service is Microsoft's cloud-based identity and directory "
      "service for authenticating users and managing access?",
      [
          "Microsoft Entra ID",
          "Azure Policy",
          "Azure Monitor",
          "Azure Resource Manager (ARM)",
      ],
      0,
      "Microsoft Entra ID is the cloud-based identity and directory service "
      "that authenticates users and manages access to resources.",
      "easy"),
    # az-900-042 -> MG.1 tags (category architecture, objective cost)
    q("az-900-042",
      "What are Azure tags?",
      [
          "Name-value pairs attached to resources for organization and cost tracking",
          "Encryption keys for storage accounts",
          "Network rules for virtual machines",
          "Password policies for users",
      ],
      0,
      "Tags are name-value pairs attached to Azure resources to organize "
      "them and track costs, for example by department or environment.",
      "easy"),
    # az-900-043 -> AA.2 private endpoint / Azure Private Link
    q("az-900-043",
      "A service must be reachable only from inside a virtual network. Which "
      "network configuration accomplishes this?",
      [
          "A private endpoint",
          "A public endpoint",
          "A subnet gateway",
          "An availability zone",
      ],
      0,
      "A private endpoint gives a service a private IP inside a virtual "
      "network so traffic stays private and does not use the public internet.",
      "medium"),
    # az-900-048 -> AA.1 regions / region pairs
    q("az-900-048",
      "What is an Azure region?",
      [
          "A geographic area containing one or more datacenters connected by a low-latency network",
          "A single physical server rack",
          "A subscription boundary",
          "A user group",
      ],
      0,
      "An Azure region is a geographic area containing one or more "
      "datacenters connected by a low-latency network.",
      "easy"),
    # az-900-049 -> AA.2 containers / Azure Container Instances
    q("az-900-049",
      "Which service offers the simplest way to run a single container in "
      "Azure without managing virtual machines or orchestration?",
      [
          "Azure Container Instances",
          "Azure Virtual Machines",
          "Azure Virtual Desktop",
          "Azure Kubernetes Service",
      ],
      0,
      "Azure Container Instances runs a container without managing VMs or an "
      "orchestrator, making it the simplest container option.",
      "medium"),
    # az-900-052 -> AA.4 single sign-on (SSO)
    q("az-900-052",
      "What does single sign-on (SSO) provide?",
      [
          "One set of credentials to access multiple applications",
          "A separate password for every application",
          "Encryption of data at rest",
          "Automatic scaling of virtual machines",
      ],
      0,
      "Single sign-on (SSO) lets a user sign in once and access multiple "
      "applications without re-entering credentials.",
      "easy"),
    # az-900-053 -> AA.4 MFA / passwordless
    q("az-900-053",
      "Which authentication method requires two or more independent factors "
      "to verify a user's identity?",
      [
          "multifactor authentication (MFA)",
          "single sign-on (SSO)",
          "passwordless",
          "federation",
      ],
      0,
      "Multifactor authentication (MFA) requires two or more independent "
      "factors, such as a password plus a phone prompt, to verify identity.",
      "medium"),
    # az-900-054 -> AA.3 redundancy options
    q("az-900-054",
      "Which redundancy option keeps three copies of data within a single "
      "datacenter in the primary region?",
      [
          "locally redundant storage (LRS)",
          "zone-redundant storage (ZRS)",
          "geo-redundant storage (GRS)",
          "geo-zone-redundant storage (GZRS)",
      ],
      0,
      "Locally redundant storage (LRS) keeps three copies of data within a "
      "single datacenter in the primary region.",
      "medium"),
    # az-900-055 -> AA.3 Azure Data Box
    q("az-900-055",
      "A company must transfer several terabytes of data to Azure but has a "
      "slow network connection. Which option is designed for this?",
      [
          "Azure Data Box",
          "AzCopy",
          "Azure File Sync",
          "Azure Storage Explorer",
      ],
      0,
      "Azure Data Box is a physical device used to transfer large amounts of "
      "data to Azure when network transfer is impractical or slow.",
      "easy"),
    # az-900-063 -> AA.2 private endpoint / Azure Private Link
    q("az-900-063",
      "Which Azure service enables the private endpoint connection into a "
      "virtual network?",
      [
          "Azure Private Link",
          "Azure VPN Gateway",
          "Azure ExpressRoute",
          "Azure DNS",
      ],
      0,
      "Azure Private Link enables private endpoints that bring a service "
      "into a virtual network over a private IP address.",
      "medium"),
    # az-900-065 -> AA.2 Azure Virtual Machines
    q("az-900-065",
      "Which service is an infrastructure as a service (IaaS) option that "
      "provides a full operating system for the customer to configure?",
      [
          "Azure Virtual Machines",
          "Azure App Service",
          "Azure Functions",
          "Azure Container Apps",
      ],
      0,
      "Azure Virtual Machines provide IaaS with a full operating system that "
      "the customer configures and manages.",
      "medium"),
    # az-900-069 -> AA.1 management groups (resource hierarchy)
    q("az-900-069",
      "Which sequence lists the Azure resource hierarchy from broadest to "
      "narrowest scope?",
      [
          "Management groups, subscriptions, resource groups, resources",
          "Resources, resource groups, subscriptions, management groups",
          "Subscriptions, management groups, resources, resource groups",
          "Resource groups, resources, management groups, subscriptions",
      ],
      0,
      "The hierarchy is management groups (broadest), then subscriptions, "
      "then resource groups, then resources (narrowest).",
      "hard"),
    # az-900-070 -> AA.2 Azure VPN Gateway
    q("az-900-070",
      "Which service creates an encrypted tunnel between an on-premises "
      "network and Azure over the public internet?",
      [
          "Azure VPN Gateway",
          "Azure ExpressRoute",
          "Azure DNS",
          "Azure Private Link",
      ],
      0,
      "Azure VPN Gateway creates an encrypted site-to-site tunnel between an "
      "on-premises network and Azure over the public internet.",
      "hard"),
    # az-900-071 -> AA.2 containers / Azure Container Apps
    q("az-900-071",
      "Which service lets you run containerized applications on a managed "
      "platform with built-in scaling?",
      [
          "Azure Container Apps",
          "Azure Virtual Desktop",
          "Azure Data Box",
          "Azure Files",
      ],
      0,
      "Azure Container Apps is a managed platform for running containerized "
      "applications with built-in scaling.",
      "hard"),
    # az-900-072 -> AA.3 storage types
    q("az-900-072",
      "Which storage service provides file shares that can be mounted using "
      "the Server Message Block (SMB) protocol?",
      [
          "Azure Files",
          "Azure Blob Storage",
          "Azure Queue Storage",
          "Azure Table Storage",
      ],
      0,
      "Azure Files provides fully managed file shares that can be mounted "
      "over SMB or NFS.",
      "medium"),
    # az-900-078 -> AA.2 availability sets (re-scoped from Azure Backup)
    q("az-900-078",
      "Which feature groups virtual machines across fault domains and update "
      "domains to improve resilience during hardware failures and planned "
      "maintenance?",
      [
          "availability sets",
          "availability zones",
          "region pairs",
          "resource groups",
      ],
      0,
      "Availability sets distribute VMs across fault domains and update "
      "domains to protect against hardware failure and planned maintenance.",
      "hard"),
    # az-900-079 -> DC.2 scalability (adjacent: autoscale)
    q("az-900-079",
      "A web app automatically adds instances when CPU rises and removes "
      "them when it falls. Which cloud benefit does this behavior provide?",
      [
          "scalability",
          "high availability",
          "disaster recovery",
          "encryption",
      ],
      0,
      "Automatically adding and removing instances to match load is "
      "scalability, one of the key benefits of cloud services.",
      "hard"),
    # az-900-080 -> AA.4 Microsoft Entra ID / directory services
    q("az-900-080",
      "Which capability does Microsoft Entra ID provide?",
      [
          "Cloud identity and directory services",
          "Network peering between virtual networks",
          "Physical storage of data",
          "Cost budgeting",
      ],
      0,
      "Microsoft Entra ID provides cloud identity and directory services, "
      "including authentication and access management.",
      "medium"),
    # az-900-081 -> AA.2 virtual network features / Azure DNS
    q("az-900-081",
      "Which service provides name resolution for Azure resources using a "
      "domain name system?",
      [
          "Azure DNS",
          "Azure VPN Gateway",
          "Azure ExpressRoute",
          "Azure Firewall",
      ],
      0,
      "Azure DNS provides name resolution for Azure resources using the "
      "domain name system.",
      "medium"),
    # az-900-086 -> AA.3 Azure Files / Azure File Sync
    q("az-900-086",
      "Which service provides fully managed file shares that multiple "
      "virtual machines can access over the network?",
      [
          "Azure Files",
          "Azure Blob Storage",
          "Azure Queue Storage",
          "Azure Data Box",
      ],
      0,
      "Azure Files provides fully managed file shares accessible by multiple "
      "virtual machines over SMB or NFS.",
      "hard"),
    # az-900-091 -> AA.1 management groups (resource hierarchy)
    q("az-900-091",
      "Which Azure object can contain subscriptions and apply governance "
      "policies to all of them at once?",
      [
          "A management group",
          "A resource group",
          "An availability set",
          "A virtual network",
      ],
      0,
      "A management group can contain subscriptions and apply governance "
      "such as Azure Policy across all of them.",
      "hard"),
    # az-900-092 -> AA.2 Azure App Service (web apps)
    q("az-900-092",
      "Which platform as a service (PaaS) option hosts web applications "
      "without the customer managing the underlying servers?",
      [
          "web apps (Azure App Service)",
          "Azure Virtual Machines",
          "Azure Virtual Desktop",
          "Azure Functions",
      ],
      0,
      "Azure App Service hosts web apps as a PaaS offering, so the customer "
      "does not manage the underlying servers.",
      "hard"),
    # az-900-093 -> DC.2 scalability (adjacent: autoscale)
    q("az-900-093",
      "Which scenario demonstrates the scalability benefit of cloud "
      "services?",
      [
          "Increasing compute resources during peak hours and reducing them afterward",
          "Restoring data from a backup after a failure",
          "Encrypting data in transit",
          "Applying a resource lock",
      ],
      0,
      "Scaling resources up during peak hours and down afterward is "
      "scalability, a core cloud benefit.",
      "hard"),
    # az-900-099 -> AA.1 regions / region pairs
    q("az-900-099",
      "What is the purpose of Azure region pairs?",
      [
          "To provide disaster recovery by pairing regions in the same geography",
          "To connect a subscription to a billing account",
          "To group virtual machines for scaling",
          "To encrypt data between regions",
      ],
      0,
      "Region pairs are two regions in the same geography used together for "
      "disaster recovery and to sequence updates.",
      "medium"),
    # az-900-100 -> AA.2 Azure Functions
    q("az-900-100",
      "Which service runs small pieces of code in response to events without "
      "managing servers?",
      [
          "Azure Functions",
          "Azure Virtual Machines",
          "Azure Virtual Desktop",
          "Azure App Service",
      ],
      0,
      "Azure Functions is a serverless compute service that runs code in "
      "response to events without managing servers.",
      "hard"),
    # az-900-101 -> AA.2 compute types
    q("az-900-101",
      "Which compute option is best described as lightweight, portable, and "
      "sharing the host operating system kernel?",
      [
          "containers",
          "virtual machines",
          "functions",
          "availability sets",
      ],
      0,
      "Containers are lightweight and portable, packaging an application "
      "with its dependencies while sharing the host operating system kernel.",
      "medium"),
    # az-900-102 -> AA.2 private endpoint / Azure Private Link
    q("az-900-102",
      "Which statement about public and private endpoints is correct?",
      [
          "A public endpoint is reachable from the internet; a private endpoint uses a private IP in a virtual network",
          "A private endpoint is always reachable from the internet",
          "Public and private endpoints are the same thing",
          "A public endpoint is only reachable on-premises",
      ],
      0,
      "A public endpoint is reachable from the internet, while a private "
      "endpoint uses a private IP address inside a virtual network.",
      "hard"),
    # az-900-109 -> AA.2 availability sets
    q("az-900-109",
      "Which concept distributes virtual machines across separate physical "
      "hardware to reduce the impact of a single hardware failure?",
      [
          "Fault domains in an availability set",
          "Resource groups",
          "Storage tiers",
          "Management groups",
      ],
      0,
      "Fault domains in an availability set place VMs on separate physical "
      "hardware so a single hardware failure does not take down all instances.",
      "hard"),
    # az-900-110 -> AA.2 containers (adjacent: Azure Container Registry)
    q("az-900-110",
      "Which compute option packages an application and its dependencies into "
      "a portable image that can run anywhere?",
      [
          "containers",
          "virtual machines",
          "availability sets",
          "region pairs",
      ],
      0,
      "Containers package an application and its dependencies into a "
      "portable image that runs consistently across environments.",
      "hard"),
    # az-900-111 -> AA.2 virtual network / subnets
    q("az-900-111",
      "Which component divides an Azure virtual network into smaller address "
      "spaces to isolate resources?",
      [
          "subnets",
          "region pairs",
          "availability zones",
          "resource groups",
      ],
      0,
      "Subnets divide a virtual network into smaller address spaces to "
      "organize and isolate resources.",
      "medium"),
    # az-900-127 -> AA.1 region pairs / cross-region replication
    q("az-900-127",
      "A company needs geographic redundancy so that if a whole Azure region "
      "fails, services continue in a second region. Which concept supports "
      "this?",
      [
          "region pairs",
          "availability zones",
          "subnets",
          "management groups",
      ],
      0,
      "Region pairs provide geographic redundancy across two regions in the "
      "same geography for disaster recovery.",
      "medium"),
    # az-900-128 -> AA.1 availability zones (reliability)
    q("az-900-128",
      "Which design choice improves reliability by keeping a workload running "
      "when one datacenter in a region fails?",
      [
          "Deploying across multiple availability zones",
          "Using a single availability zone",
          "Putting all resources in one resource group",
          "Using one storage account",
      ],
      0,
      "Deploying across multiple availability zones keeps a workload running "
      "when a single datacenter in the region fails.",
      "hard"),
    # az-900-129 -> AA.2 availability sets
    q("az-900-129",
      "Which feature keeps virtual machines available during Azure planned "
      "maintenance by placing them in separate update domains?",
      [
          "An availability set",
          "An availability zone",
          "A management group",
          "A network security group",
      ],
      0,
      "An availability set places virtual machines in separate update "
      "domains so planned maintenance does not reboot all instances at once.",
      "medium"),
    # ---- gap items (7 outline topics the legacy bank never covered) ----
    # az-900-134 -> AA.2 Azure Virtual Desktop
    q("az-900-134",
      "Which service provides virtualized desktops and applications that "
      "users access from anywhere?",
      [
          "Azure Virtual Desktop",
          "Azure Virtual Machines",
          "Azure App Service",
          "Azure Functions",
      ],
      0,
      "Azure Virtual Desktop delivers virtualized desktops and applications "
      "that users access remotely.",
      "medium"),
    # az-900-135 -> AA.1 sovereign regions
    q("az-900-135",
      "A government agency needs Azure services that are physically and "
      "logically isolated from commercial Azure regions to satisfy national "
      "legal requirements. Which region type provides this?",
      [
          "sovereign regions",
          "availability zones",
          "resource groups",
          "virtual networks",
      ],
      0,
      "Sovereign regions are physically and logically isolated Azure "
      "environments for customers with strict legal or compliance "
      "requirements, such as government agencies.",
      "medium"),
    # az-900-136 -> AA.4 Microsoft Entra Domain Services
    q("az-900-136",
      "Which service provides managed domain services such as domain join and "
      "group policy without the customer running domain controllers?",
      [
          "Microsoft Entra Domain Services",
          "Microsoft Entra ID",
          "Azure Policy",
          "Azure Monitor",
      ],
      0,
      "Microsoft Entra Domain Services provides managed domain services such "
      "as domain join and group policy without self-managed controllers.",
      "medium"),
    # az-900-137 -> AA.4 external identities
    q("az-900-137",
      "Which Microsoft Entra capability lets you invite users from outside "
      "your organization to access your applications?",
      [
          "external identities",
          "single sign-on (SSO)",
          "passwordless",
          "multifactor authentication (MFA)",
      ],
      0,
      "External identities let you invite users outside your organization, "
      "such as partners and customers, to access your applications.",
      "medium"),
    # az-900-138 -> AA.3 AzCopy
    q("az-900-138",
      "Which command-line tool copies blobs and files to and from Azure "
      "storage accounts?",
      [
          "AzCopy",
          "Azure Storage Explorer",
          "Azure File Sync",
          "Azure Data Box",
      ],
      0,
      "AzCopy is a command-line tool for copying blobs and files to and from "
      "Azure storage accounts.",
      "medium"),
    # az-900-139 -> AA.3 Azure File Sync
    q("az-900-139",
      "Which service synchronizes an on-premises file server with an Azure "
      "file share so files are available in both locations?",
      [
          "Azure File Sync",
          "AzCopy",
          "Azure Data Box",
          "Azure Migrate",
      ],
      0,
      "Azure File Sync synchronizes on-premises file servers with Azure "
      "Files so the same files are available in both locations.",
      "medium"),
    # az-900-140 -> AA.3 Azure Storage Explorer
    q("az-900-140",
      "Which graphical tool lets you manage Azure storage accounts, blobs, "
      "files, and queues from a desktop application?",
      [
          "Azure Storage Explorer",
          "AzCopy",
          "Azure Cloud Shell",
          "Azure PowerShell",
      ],
      0,
      "Azure Storage Explorer is a desktop application for managing Azure "
      "storage accounts, blobs, files, and queues graphically.",
      "medium"),
]
