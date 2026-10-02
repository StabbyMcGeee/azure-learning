"""AZ-900 cloud-concepts replacement items (fresh originals).

Each item replaces the legacy slot with a new original authored from the
public AZ-900 skills outline (July 20, 2026) and standard Microsoft Learn facts.
Legacy wording was not read or reused; only the public objective and exact
official Azure term from the coverage map were followed.
"""

SRC = (
    "Original AI-fleet-authored content with publisher review (Dimitri Meier); "
    "facts from Microsoft Learn, retrieved 2026-10-02"
)
BASIS = "original-human-ai-assisted"
COURSE = "az-900"

QUESTIONS = [
    # az-900-001 -> DC.1 cloud computing
    {
        "id": "az-900-001",
        "text": (
            "A startup needs computing power, storage, and networking but does "
            "not want to buy or maintain its own hardware. Which term best "
            "describes the delivery model it should use?"
        ),
        "options": [
            "cloud computing",
            "on-premises data center",
            "edge computing",
            "colocation",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Cloud computing delivers computing services such as servers, "
            "storage, and networking over the internet on a pay-as-you-go "
            "basis, so the customer does not own or maintain the physical "
            "infrastructure."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "easy",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-002 -> DC.1 consumption-based model / pay-as-you-go
    {
        "id": "az-900-002",
        "text": (
            "Which characteristic describes the consumption-based model of "
            "cloud services?"
        ),
        "options": [
            "You pay only for the resources you use.",
            "You must buy fixed capacity in advance.",
            "You are billed the same amount every month regardless of use.",
            "You always pay a fixed up-front hardware cost.",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "In a consumption-based model you pay only for what you use and "
            "you stop incurring charges when you stop using the resources. "
            "Buying fixed capacity up front is capital expenditure, not "
            "consumption-based pay-as-you-go."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-003 -> DC.1 shared responsibility model
    {
        "id": "az-900-003",
        "text": (
            "Under the shared responsibility model, which party is always "
            "responsible for the physical security of the cloud datacenter?"
        ),
        "options": [
            "the cloud provider",
            "the customer",
            "the customer's security vendor",
            "both the customer and the provider equally",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "The shared responsibility model assigns responsibility for the "
            "physical security of datacenters, hosts, and networks to the "
            "cloud provider. The customer remains responsible for its data, "
            "endpoints, accounts, and access management."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-004 -> DC.2 scalability
    {
        "id": "az-900-004",
        "text": (
            "A retail website doubles the number of virtual machines running "
            "its storefront during a holiday sale, then reduces them "
            "afterward. Which cloud benefit does this describe?"
        ),
        "options": [
            "scalability",
            "disaster recovery",
            "encryption",
            "compliance",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Scalability is the ability to add or remove resources to meet "
            "changing demand, such as scaling out during peak traffic and "
            "scaling back in afterward."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "easy",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-005 -> DC.2 cloud benefits
    {
        "id": "az-900-005",
        "text": (
            "A team adopts a cloud service that is managed through a web "
            "portal, a command-line interface, and APIs without needing to "
            "visit a datacenter. Which benefit of cloud services is most "
            "directly demonstrated?"
        ),
        "options": [
            "manageability",
            "scalability",
            "high availability",
            "disaster recovery",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Manageability describes how easily a cloud solution can be "
            "operated and monitored through a portal, CLI, or API rather "
            "than through physical datacenter visits."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-006 -> DC.1 public/private/hybrid cloud
    {
        "id": "az-900-006",
        "text": (
            "A company runs some workloads in its own datacenter and other "
            "workloads in a public cloud, with data moving between them. "
            "Which cloud model does this describe?"
        ),
        "options": [
            "hybrid cloud",
            "public cloud",
            "private cloud",
            "community cloud",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "A hybrid cloud combines a private cloud or on-premises "
            "datacenter with a public cloud, allowing data and applications "
            "to be shared between them."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-007 -> DC.1 serverless
    {
        "id": "az-900-007",
        "text": (
            "Which term describes a cloud compute model where the provider "
            "manages the servers and automatically scales resources as "
            "events arrive?"
        ),
        "options": [
            "serverless",
            "a dedicated physical server",
            "a virtual machine that the developer fully maintains",
            "a colocated rack",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Serverless computing abstracts away server management; the "
            "provider handles infrastructure and the code runs on demand, "
            "typically in response to events."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-008 -> DC.2 cloud benefits
    {
        "id": "az-900-008",
        "text": (
            "A workload automatically adds resources when traffic rises. "
            "Which cloud benefit does this illustrate?"
        ),
        "options": [
            "scalability",
            "physical security",
            "data residency",
            "licensing",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Scalability is the ability to add or remove resources to match "
            "changing demand, such as automatically adding resources when "
            "traffic rises."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "easy",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-041 -> DC.2 cloud benefits
    {
        "id": "az-900-041",
        "text": (
            "A cloud workload keeps running during a datacenter outage "
            "because it is distributed across multiple locations. Which "
            "benefit is illustrated?"
        ),
        "options": [
            "high availability",
            "scalability",
            "manageability",
            "governance",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "High availability means a service remains available even when "
            "individual components or locations fail, often through "
            "redundancy across multiple locations."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "easy",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-045 -> DC.2 cloud benefits
    {
        "id": "az-900-045",
        "text": (
            "Cloud services can offer predictable cost and predictable "
            "performance. Which statement about predictability is correct?"
        ),
        "options": [
            "Predictability comes from features such as autoscaling and cost tracking.",
            "Predictability means every workload always costs exactly zero.",
            "Predictability removes the need to monitor spending.",
            "Predictability guarantees a fixed monthly bill for every service.",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Predictability in the cloud comes from capabilities such as "
            "autoscaling for performance and cost-tracking tools for "
            "spending; it does not mean costs are always zero or fixed."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-046 -> DC.1 cloud computing
    {
        "id": "az-900-046",
        "text": (
            "Which phrase best defines cloud computing?"
        ),
        "options": [
            "Delivery of computing services over the internet with pay-as-you-go pricing",
            "Running software only on a laptop",
            "Backing up files to an external hard drive",
            "Hosting a website on a single office server",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Cloud computing delivers computing services such as compute, "
            "storage, and networking over the internet with pay-as-you-go "
            "pricing."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "easy",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-047 -> DC.1 cloud models / cloud service types
    {
        "id": "az-900-047",
        "text": (
            "Which cloud model provides shared, multi-tenant resources over "
            "the internet to the general public?"
        ),
        "options": [
            "public cloud",
            "private cloud",
            "hybrid cloud",
            "community cloud",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "A public cloud provides shared, multi-tenant resources over "
            "the internet to the general public, in contrast to a private "
            "cloud dedicated to a single organization."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-067 -> DC.1 shared responsibility model
    {
        "id": "az-900-067",
        "text": (
            "In the shared responsibility model, who is responsible for "
            "protecting customer data and managing user accounts and access?"
        ),
        "options": [
            "the customer",
            "the cloud provider",
            "the hardware vendor",
            "nobody, because the provider handles everything",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "The customer is always responsible for its data, endpoints, "
            "accounts, and access management, while the cloud provider "
            "protects the underlying physical infrastructure."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-068 -> DC.3 IaaS / PaaS / SaaS
    {
        "id": "az-900-068",
        "text": (
            "In which cloud service type does the provider fully manage the "
            "application and infrastructure while the customer only uses the "
            "software?"
        ),
        "options": [
            "software as a service (SaaS)",
            "infrastructure as a service (IaaS)",
            "platform as a service (PaaS)",
            "serverless",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "In SaaS the provider fully manages the application and "
            "infrastructure, and the customer only uses the software. In "
            "IaaS and PaaS the customer retains more management responsibility."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-077 -> MG.1 Microsoft Cost Management
    {
        "id": "az-900-077",
        "text": (
            "Which tool helps you analyze cloud spending, set budgets, and "
            "identify underused resources to control costs?"
        ),
        "options": [
            "Microsoft Cost Management",
            "Azure Monitor",
            "Azure Advisor",
            "Azure Policy",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Microsoft Cost Management provides cost analysis, budgets, and "
            "recommendations for controlling and optimizing cloud spending."
        ),
        "domain": "Azure Management and Governance",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-085 -> DC.2 reliability / predictability
    {
        "id": "az-900-085",
        "text": (
            "Reliability is the ability of a system to recover from failures "
            "and continue to function. Which design approach best supports "
            "reliability in the cloud?"
        ),
        "options": [
            "Distributing resources across multiple regions or availability zones",
            "Running everything on one server in one location",
            "Avoiding any monitoring or telemetry",
            "Relying on a single power source",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Reliability is improved by distributing resources across "
            "multiple regions or availability zones so the system can "
            "recover from failures and keep functioning."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "hard",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-087 -> AA.3 Azure Migrate (re-scoped from "6 Rs")
    {
        "id": "az-900-087",
        "text": (
            "An organization wants to move its existing on-premises servers "
            "and databases to Azure and needs a hub of tools to assess and "
            "carry out the migration. Which service is designed for this?"
        ),
        "options": [
            "Azure Migrate",
            "Azure Data Box",
            "Azure Backup",
            "Azure ExpressRoute",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Azure Migrate is a service that provides tools to discover, "
            "assess, and migrate on-premises servers, databases, and web "
            "apps to Azure."
        ),
        "domain": "Azure Architecture and Services",
        "difficulty": "hard",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-088 -> DC.3 IaaS / PaaS / SaaS
    {
        "id": "az-900-088",
        "text": (
            "With infrastructure as a service (IaaS), which layers does the "
            "customer manage?"
        ),
        "options": [
            "The operating system and applications",
            "The physical datacenter and network hardware",
            "Nothing, because the provider manages everything",
            "Only the billing",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "With IaaS the customer manages the operating system and "
            "applications while the cloud provider manages the physical "
            "infrastructure such as servers, storage, and networking."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-089 -> DC.2 scalability
    {
        "id": "az-900-089",
        "text": (
            "Which action represents scaling out to meet an increase in "
            "demand?"
        ),
        "options": [
            "Adding more virtual machines during a traffic spike",
            "Replacing a failed hard drive",
            "Encrypting data at rest",
            "Creating a backup copy",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Scaling out adds more instances, such as virtual machines, to "
            "meet increased demand. Replacing failed hardware is fault "
            "tolerance, not scaling."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "hard",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-097 -> DC.1 cloud computing
    {
        "id": "az-900-097",
        "text": (
            "A company moves from buying servers every few years to renting "
            "compute capacity billed monthly. Which spending model change "
            "does this represent?"
        ),
        "options": [
            "From capital expenditure to operational expenditure",
            "From operational expenditure to capital expenditure",
            "From fixed to fixed, with no change",
            "From subscription to one-time purchase",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Renting cloud capacity converts up-front capital expenditure "
            "(CapEx) on hardware into ongoing operational expenditure "
            "(OpEx) billed as it is used."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-098 -> DC.2 reliability / predictability
    {
        "id": "az-900-098",
        "text": (
            "Which factor contributes most directly to predictable cloud "
            "costs?"
        ),
        "options": [
            "Monitoring usage with cost-tracking tools",
            "Ignoring resource usage after deployment",
            "Removing all tags from resources",
            "Avoiding the pricing calculator",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Predictable costs come from monitoring usage with cost-tracking "
            "tools and understanding consumption-based pricing. Ignoring "
            "usage or removing tags reduces cost predictability."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "hard",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-107 -> DC.1 cloud computing / cloud models
    {
        "id": "az-900-107",
        "text": (
            "An organization that must keep workloads entirely within its own "
            "datacenter, with no shared multi-tenant hardware, should use "
            "which cloud model?"
        ),
        "options": [
            "private cloud",
            "public cloud",
            "hybrid cloud",
            "serverless",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "A private cloud dedicates resources to a single organization, "
            "either in its own datacenter or a hosted one, without shared "
            "multi-tenant hardware."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-108 -> DC.2 cloud benefits (re-scoped from Cloud Adoption Framework)
    {
        "id": "az-900-108",
        "text": (
            "Which benefit of cloud services typically motivates an "
            "organization to adopt the cloud?"
        ),
        "options": [
            "Scaling resources to match demand",
            "Guaranteed elimination of all security risks",
            "Removing the need to manage any data",
            "Permanent ownership of the datacenter",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Cloud adoption is commonly driven by scalability and the "
            "reduction of up-front capital costs. It does not eliminate "
            "security responsibilities or the need to manage data."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-116 -> DC.1 cloud computing
    {
        "id": "az-900-116",
        "text": (
            "Which of the following is a defining feature of cloud computing?"
        ),
        "options": [
            "On-demand self-service provisioning of resources",
            "Permanent ownership of physical servers",
            "Manual capacity planning for every request",
            "Access limited to a single physical location",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Cloud computing is characterized by on-demand self-service, "
            "broad network access, resource pooling, rapid elasticity, and "
            "measured (pay-as-you-go) service."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-117 -> DC.1 shared responsibility model
    {
        "id": "az-900-117",
        "text": (
            "As a customer moves from IaaS to PaaS to SaaS, how does the "
            "customer's share of responsibility change?"
        ),
        "options": [
            "The customer's responsibility decreases.",
            "The customer's responsibility increases.",
            "The customer's responsibility stays exactly the same.",
            "The provider's responsibility disappears.",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Moving from IaaS to PaaS to SaaS shifts more management to the "
            "cloud provider, so the customer's share of responsibility "
            "decreases."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-118 -> DC.1 cloud computing
    {
        "id": "az-900-118",
        "text": (
            "A business pays only for the compute seconds it actually "
            "consumes, with no long-term commitment. Which cloud pricing "
            "model is this?"
        ),
        "options": [
            "pay-as-you-go",
            "reserved capacity",
            "a perpetual software license",
            "a fixed hardware lease",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Pay-as-you-go billing charges only for what is consumed with no "
            "up-front or long-term commitment, which is a core part of the "
            "consumption-based model."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-119 -> DC.1 cloud computing / cloud models
    {
        "id": "az-900-119",
        "text": (
            "Which statement correctly contrasts a public cloud with a "
            "private cloud?"
        ),
        "options": [
            "A public cloud shares resources across organizations; a private cloud is dedicated to one organization.",
            "A public cloud is always on-premises; a private cloud is always hosted by a third party.",
            "A private cloud always has lower security than a public cloud.",
            "Public and private clouds are the same thing.",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "A public cloud provides shared, multi-tenant resources over the "
            "internet, while a private cloud dedicates resources to a single "
            "organization."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-120 -> DC.1 cloud computing
    {
        "id": "az-900-120",
        "text": (
            "Which benefit of cloud computing lets a team provision a new "
            "development environment in minutes without contacting a "
            "datacenter operator?"
        ),
        "options": [
            "On-demand self-service",
            "Manual hardware installation",
            "Fixed-term contracts",
            "On-premises maintenance",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "On-demand self-service lets users provision resources through a "
            "portal or API immediately, without manual datacenter work."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-121 -> DC.1 cloud computing
    {
        "id": "az-900-121",
        "text": (
            "Cloud computing uses a consumption-based model. Which statement "
            "about this model is true?"
        ),
        "options": [
            "You pay for the resources you consume, and charges stop when you stop using them.",
            "You must buy all capacity up front.",
            "You are charged a fixed annual fee no matter what you use.",
            "You own the cloud provider's hardware.",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "The consumption-based model charges for actual use and stops "
            "accruing cost when resources are released; it does not require "
            "up-front purchase of all capacity."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-122 -> MG.1 Azure Reservations
    {
        "id": "az-900-122",
        "text": (
            "A company has steady, predictable virtual machine usage and "
            "wants a lower price in exchange for a one- or three-year "
            "commitment. Which option should it consider?"
        ),
        "options": [
            "Azure Reservations",
            "Azure Spot Virtual Machines",
            "Pay-as-you-go with no commitment",
            "A free trial",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Azure Reservations offer a discounted price in exchange for a "
            "one- or three-year commitment on eligible resources, suited to "
            "steady, predictable workloads."
        ),
        "domain": "Azure Management and Governance",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-123 -> MG.1 Azure Spot Virtual Machines
    {
        "id": "az-900-123",
        "text": (
            "Which purchase option provides large discounts on unused Azure "
            "compute capacity but can be interrupted when capacity is needed "
            "elsewhere?"
        ),
        "options": [
            "Azure Spot Virtual Machines",
            "Azure Reservations",
            "Azure Hybrid Benefit",
            "Pay-as-you-go reserved instances",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "Azure Spot Virtual Machines offer deep discounts on unused "
            "capacity but can be evicted when Azure needs the capacity back, "
            "so they suit interruptible workloads."
        ),
        "domain": "Azure Management and Governance",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
    # az-900-133 -> DC.1 cloud computing / models / service types
    {
        "id": "az-900-133",
        "text": (
            "Which of the following is a cloud service type?"
        ),
        "options": [
            "infrastructure as a service (IaaS)",
            "private cloud",
            "hybrid cloud",
            "public cloud",
        ],
        "correctOptionIndex": 0,
        "explanation": (
            "IaaS is one of the three cloud service types, along with PaaS "
            "and SaaS. Private, hybrid, and public are deployment models, "
            "not service types."
        ),
        "domain": "Cloud Concepts",
        "difficulty": "medium",
        "source": SRC,
        "rightsBasis": BASIS,
        "courseId": COURSE,
    },
]
