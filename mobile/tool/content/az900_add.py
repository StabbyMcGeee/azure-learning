"""AZ-900 additions to align weighting to the study guide and fill gaps.

Adds cloud-concepts items to lift the DC share into its 25-30% band and adds
the two missing-objective items (storage tiers, defense-in-depth) plus two
management items.
"""

SRC = (
    "Original AI-fleet-authored content with publisher review (Dimitri Meier); "
    "facts from Microsoft Learn AZ-900 study guide (2026-07-20) and docs, "
    "retrieved 2026-10-02"
)
BASIS = "original-human-ai-assisted"
COURSE = "az-900"

DC = "Cloud Concepts"
AA = "Azure Architecture and Services"
MG = "Azure Management and Governance"


def q(id_, domain, text, options, ci, expl, diff="medium"):
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
    q("az-900-141", DC,
      "Which term describes the on-demand delivery of computing services such "
      "as servers, storage, and databases over the internet?",
      ["cloud computing", "edge computing", "colocation", "virtualization"],
      0,
      "Cloud computing delivers computing services such as servers, storage, "
      "and databases over the internet on demand.",
      "easy"),
    q("az-900-142", DC,
      "Under the shared responsibility model for a SaaS application, which "
      "item remains the customer's responsibility?",
      ["Their data and user accounts",
       "The physical datacenter",
       "The application code",
       "The network hardware"],
      0,
      "Even with SaaS the customer remains responsible for its data, "
      "endpoints, and account access management.",
      "medium"),
    q("az-900-143", DC,
      "Which cloud model is best for an organization that must keep data on "
      "hardware it owns and controls in its own datacenter?",
      ["private cloud", "public cloud", "hybrid cloud", "serverless"],
      0,
      "A private cloud dedicates hardware to a single organization, giving it "
      "full control in its own datacenter.",
      "easy"),
    q("az-900-144", DC,
      "Which pricing approach charges for the resources actually consumed, "
      "with no up-front purchase?",
      ["consumption-based model", "capital expenditure", "a perpetual license",
       "a fixed hardware lease"],
      0,
      "The consumption-based model charges for actual resource use with no "
      "up-front purchase, unlike capital expenditure.",
      "medium"),
    q("az-900-145", DC,
      "Which benefit of cloud services provides safeguards that help protect "
      "data and applications from threats?",
      ["security", "scalability", "high availability", "manageability"],
      0,
      "Security is a benefit of cloud services, delivered through controls "
      "that protect data, applications, and infrastructure.",
      "medium"),
    q("az-900-146", DC,
      "Which benefit keeps a workload available during a datacenter failure "
      "by running it across multiple locations?",
      ["high availability", "scalability", "predictability", "governance"],
      0,
      "High availability keeps a workload available during failures by using "
      "redundancy across multiple locations.",
      "medium"),
    q("az-900-147", DC,
      "Which benefit describes having predictable performance and predictable "
      "cost?",
      ["predictability", "scalability", "security", "manageability"],
      0,
      "Predictability means both performance and cost can be anticipated, "
      "supported by autoscaling and cost-tracking tools.",
      "medium"),
    q("az-900-148", DC,
      "Which benefit of cloud services lets an organization apply policies and "
      "controls consistently across its resources?",
      ["governance", "scalability", "high availability", "reliability"],
      0,
      "Governance lets an organization apply policies and controls "
      "consistently across cloud resources.",
      "medium"),
    q("az-900-149", DC,
      "Which cloud service type requires the customer to manage the operating "
      "system and applications?",
      ["infrastructure as a service (IaaS)",
       "platform as a service (PaaS)",
       "software as a service (SaaS)",
       "serverless"],
      0,
      "With IaaS the customer manages the operating system and applications, "
      "while the provider manages the physical infrastructure.",
      "medium"),
    q("az-900-150", DC,
      "Microsoft 365, which delivers fully managed productivity applications "
      "over the internet, is an example of which service type?",
      ["software as a service (SaaS)",
       "infrastructure as a service (IaaS)",
       "platform as a service (PaaS)",
       "serverless"],
      0,
      "Microsoft 365 is software as a service (SaaS): the provider fully "
      "manages the applications and infrastructure.",
      "easy"),
    q("az-900-151", DC,
      "Which cloud service type provides a managed platform for developing "
      "and deploying applications without managing the underlying "
      "infrastructure?",
      ["platform as a service (PaaS)",
       "infrastructure as a service (IaaS)",
       "software as a service (SaaS)",
       "a physical datacenter"],
      0,
      "PaaS provides a managed platform (runtime, middleware, tools) so "
      "developers do not manage the underlying infrastructure.",
      "medium"),
    q("az-900-152", DC,
      "Which compute approach runs code only when needed and bills only for "
      "the compute time used, with the provider managing the servers?",
      ["serverless", "a dedicated physical server", "a colocated rack",
       "a virtual machine managed by the customer"],
      0,
      "Serverless runs code on demand and bills for actual execution, with "
      "the provider managing the servers.",
      "medium"),
    q("az-900-153", MG,
      "Which tool provides a graphical web interface for creating and "
      "managing Azure resources?",
      ["Azure portal", "Azure Cloud Shell", "Azure CLI", "Azure PowerShell"],
      0,
      "The Azure portal is the graphical web interface for creating and "
      "managing Azure resources.",
      "easy"),
    q("az-900-154", MG,
      "An administrator must prevent accidental deletion of a critical "
      "storage account. Which feature should they apply?",
      ["A resource lock", "A tag", "An Azure Advisor recommendation",
       "A role assignment"],
      0,
      "A resource lock (read-only or delete) prevents accidental deletion or "
      "modification of a resource such as a storage account.",
      "medium"),
    q("az-900-155", AA,
      "Which Azure Blob storage tier offers the lowest storage cost for data "
      "that is rarely accessed and can tolerate retrieval latency of hours?",
      ["Archive tier", "Hot tier", "Cool tier", "Cold tier"],
      0,
      "The archive tier has the lowest storage cost for rarely accessed data "
      "that can tolerate retrieval latency of hours.",
      "medium"),
    q("az-900-156", AA,
      "Which security model protects a workload by layering multiple "
      "independent controls so a failure in one layer does not expose the "
      "whole system?",
      ["defense-in-depth", "Zero Trust", "the shared responsibility model",
       "single sign-on (SSO)"],
      0,
      "defense-in-depth layers multiple independent security controls so that "
      "one failing layer does not compromise the whole system.",
      "medium"),
]
