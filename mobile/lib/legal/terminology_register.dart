/// Terminology consistency register derived from azlegal-db-v1 section 2.
///
/// The register records the exact wording that may appear in pack content for
/// each launch course. It also records retired/predecessor wording and
/// ambiguous abbreviations that must be qualified in a course-specific way.
class TerminologyRegister {
  const TerminologyRegister._();

  static const List<String> allCourses = ['az-900', 'sc-900', 'ai-901', 'dp-900'];

  /// Returns true when [courseId] is one of the launch courses covered by the
  /// register. The pack validator uses this to reject unknown/typo courseIds
  /// instead of silently skipping terminology checks.
  static bool isKnownCourse(String courseId) => allCourses.contains(courseId);

  /// Verified exact terms grouped by the courses where they are current.
  ///
  /// A term only needs to appear in the list for the course it is used in.
  /// Cross-course terms are duplicated when the register calls out a
  /// course-scoped label (e.g. "Zero Trust" vs "Zero Trust model").
  static const Map<String, List<String>> verifiedTerms = {
    'az-900': [
      'cloud computing',
      'public cloud',
      'private cloud',
      'hybrid cloud',
      'consumption-based model',
      'cloud pricing models',
      'pay-as-you-go',
      'serverless',
      'high availability',
      'scalability',
      'reliability',
      'predictability',
      'security',
      'governance',
      'manageability',
      'infrastructure as a service (IaaS)',
      'platform as a service (PaaS)',
      'software as a service (SaaS)',
      'Azure regions',
      'region pairs',
      'sovereign regions',
      'availability zones',
      'Azure datacenters',
      'Azure resources',
      'resource groups',
      'subscriptions',
      'management groups',
      'containers',
      'virtual machines',
      'functions',
      'Azure Virtual Machines',
      'Azure Virtual Machine Scale Sets',
      'availability sets',
      'Azure Virtual Desktop',
      'web apps (Azure App Service)',
      'Azure Virtual Network',
      'subnets',
      'virtual network peering',
      'Azure DNS',
      'Azure VPN Gateway',
      'Azure ExpressRoute',
      'public endpoint',
      'private endpoint (Azure Private Link)',
      'Azure Storage services',
      'storage tiers',
      'redundancy options',
      'storage account',
      'storage types',
      'locally redundant storage (LRS)',
      'zone-redundant storage (ZRS)',
      'geo-redundant storage (GRS)',
      'geo-zone-redundant storage (GZRS)',
      'AzCopy',
      'Azure Storage Explorer',
      'Azure File Sync',
      'Azure Migrate',
      'Azure Data Box',
      'directory services',
      'Microsoft Entra ID',
      'Microsoft Entra Domain Services',
      'single sign-on (SSO)',
      'multifactor authentication (MFA)',
      'passwordless',
      'external identities',
      'Microsoft Entra Conditional Access',
      'Azure role-based access control (RBAC)',
      'Zero Trust',
      'defense-in-depth',
      'Microsoft Defender for Cloud',
      'Microsoft Cost Management',
      'pricing calculator',
      'tags',
      'Microsoft Purview',
      'Azure Policy',
      'resource locks',
      'Azure portal',
      'Azure Cloud Shell',
      'Azure CLI',
      'Azure PowerShell',
      'Azure Arc',
      'infrastructure as code (IaC)',
      'Azure Resource Manager (ARM)',
      'ARM templates',
      'Azure Advisor',
      'Azure Service Health',
      'Azure Monitor',
      'Log Analytics',
      'Azure Monitor alerts',
      'Azure Monitor Application Insights',
      'shared responsibility model',
      'Azure App Service',
      'Azure Arc Resource Bridge',
      'Azure Arc-enabled Kubernetes',
      'Azure Blob Storage',
      'Azure Container Apps',
      'Azure Container Instances',
      'Azure Files',
      'Azure Firewall',
      'Azure Front Door',
      'Azure Functions',
      'Azure Hybrid Benefit',
      'Azure Kubernetes Service',
      'Azure Private Link',
      'Azure Queue Storage',
      'Azure Reservations',
      'Azure Resource Health',
      'Azure Spot Virtual Machines',
      'Azure Table Storage',
      'SQL Server',
      'SQL Managed Instance',
    ],
    'sc-900': [
      'shared responsibility model',
      'defense-in-depth',
      'Zero Trust model',
      'encryption',
      'hashing',
      'security, compliance, and identity (SCI)',
      'Governance, Risk, and Compliance (GRC)',
      'identity as the primary security perimeter',
      'authentication',
      'authorization',
      'identity providers',
      'directory services and Active Directory',
      'federation',
      'Microsoft Entra ID',
      'workload identities',
      'hybrid identity',
      'authentication methods',
      'multifactor authentication (MFA)',
      'password protection',
      'Microsoft Entra Conditional Access',
      'Microsoft Entra roles',
      'role-based access control (RBAC)',
      'Microsoft Entra ID Governance',
      'access reviews',
      'Microsoft Entra Privileged Identity Management',
      'Microsoft Entra ID Protection',
      'Azure DDoS Protection',
      'Azure Firewall',
      'Azure Web Application Firewall (WAF)',
      'network security groups (NSGs)',
      'Azure Bastion',
      'Azure Key Vault',
      'Microsoft Defender for Cloud',
      'Cloud Security Posture Management (CSPM)',
      'security policies, standards, and recommendations',
      'cloud workload protection',
      'Microsoft Sentinel',
      'security information and event management (SIEM)',
      'security orchestration automated response (SOAR)',
      'Microsoft Defender XDR',
      'Microsoft Defender for Office 365',
      'Microsoft Defender for Endpoint',
      'Microsoft Defender for Cloud Apps',
      'Microsoft Defender for Identity',
      'Microsoft Defender Vulnerability Management',
      'Microsoft Threat Intelligence',
      'Microsoft Defender portal',
      'Microsoft Service Trust Portal',
      'privacy principles',
      'Microsoft Purview portal',
      'Compliance Manager',
      'compliance score',
      'data classification',
      'Content explorer',
      'Activity explorer',
      'sensitivity labels',
      'sensitivity label policies',
      'data loss prevention (DLP)',
      'records management',
      'retention policies',
      'retention labels',
      'retention label policies',
      'insider risk management',
      'eDiscovery',
      'audit',
    ],
    'ai-901': [
      'responsible AI',
      'fairness',
      'reliability and safety',
      'privacy and security',
      'inclusiveness',
      'transparency',
      'accountability',
      'generative AI models',
      'AI model components and configurations',
      'model deployment options',
      'configuration parameters',
      'AI workloads: generative and agentic AI',
      'text analysis',
      'speech',
      'computer vision',
      'information extraction',
      'keyword extraction',
      'entity detection',
      'sentiment analysis',
      'summarization',
      'speech recognition',
      'speech synthesis',
      'image-generation models',
      'Microsoft Foundry',
      'Foundry portal',
      'Foundry SDK',
      'single-agent solution',
      'multimodal model',
      'Azure Speech in Foundry Tools',
      'Azure Content Understanding in Foundry Tools',
      'Content Understanding',
      'Azure Blob Storage',
      'Azure Cosmos DB',
      'Azure Databricks',
      'Azure Files',
      'Foundry Tools',
      'SQL',
    ],
    'dp-900': [
      'Azure Blob Storage',
      'Azure Cosmos DB',
      'Azure Cosmos DB API',
      'Azure Data Explorer',
      'Azure Data Factory',
      'Azure Data Lake Storage',
      'Azure Database',
      'Azure Databricks',
      'Azure Event Hubs',
      'Azure Files',
      'Azure PaaS',
      'Azure SQL Database',
      'Azure SQL Managed Instance',
      'Azure Stream Analytics',
      'Azure Table Storage',
      'Azure Virtual Machines',
      'Microsoft Fabric',
      'Microsoft Power BI',
      'Power BI',
      'SQL Server',
      'SQL-like',
    ],
  };

  /// Substrings that strongly suggest a Microsoft/Azure product or feature
  /// name. The linter only flags unverified *product* terms; generic concepts
  /// like "elasticity" or "CapEx" are not treated as product terms.
  static const List<String> productTermMarkers = [
    'azure',
    'microsoft',
    'entra',
    'defender',
    'purview',
    'sentinel',
    'foundry',
    'intune',
    'fabric',
    'power',
    'sharepoint',
    'exchange',
    'teams',
    'dynamics',
    'sql',
    'cosmos',
    'synapse',
    'blob',
    'files',
    'queues',
    'tables',
    'key vault',
    'firewall',
    'ddos',
    'waf',
  ];

  /// Common misspellings or incorrect variants of official terms, mapped to
  /// the exact expected wording. The linter reports the expected value.
  static const Map<String, String> knownMisspellings = {
    'defence-in-depth': 'defense-in-depth',
    'multi-factor authentication': 'multifactor authentication (MFA)',
    'multi factor authentication': 'multifactor authentication (MFA)',
    'geo-redundant zones': 'geo-zone-redundant storage (GZRS) under "redundancy options"',
  };

  /// Ambiguous abbreviations and the exact qualified phrase each course requires.
  ///
  /// The linter accepts a bare abbreviation only when the course-qualified
  /// phrase is present in the same field. Otherwise the build fails with the
  /// expected phrase.
  static const Map<String, Map<String, String>> ambiguousAcronyms = {
    'RBAC': {
      'az-900': 'Azure role-based access control (RBAC)',
      'sc-900': 'Microsoft Entra roles and role-based access control (RBAC)',
    },
  };

  /// Retired, renamed, or otherwise non-exam wording that must not appear in
  /// pack content. The replacement string is the exact expected wording.
  static const List<RetiredTerm> retiredTerms = [
    RetiredTerm(
      pattern: 'Azure AD',
      replacement: 'Microsoft Entra ID',
      courses: allCourses,
    ),
    RetiredTerm(
      pattern: 'Azure Active Directory',
      replacement: 'Microsoft Entra ID',
      courses: allCourses,
    ),
    RetiredTerm(
      pattern: 'Azure Security Center',
      replacement: 'Microsoft Defender for Cloud',
      courses: allCourses,
    ),
    RetiredTerm(
      pattern: 'Azure Defender',
      replacement: 'Microsoft Defender for Cloud',
      courses: allCourses,
    ),
    RetiredTerm(
      pattern: 'Azure Blueprints',
      replacement: 'deprecated/not in outline (do not use)',
      courses: allCourses,
    ),
    // These AI-901 study-resource terms are stale only within the ai-901
    // course context; they may still be legitimate words in AZ-900/SC-900
    // scenarios, so the linter scopes them to ai-901 only.
    RetiredTerm(
      pattern: 'LUIS',
      replacement: 'do not use retired AI-901 study-resource wording',
      courses: ['ai-901'],
    ),
    RetiredTerm(
      pattern: 'Language Understanding',
      replacement: 'do not use retired AI-901 study-resource wording',
      courses: ['ai-901'],
    ),
    RetiredTerm(
      pattern: 'Anomaly Detector',
      replacement: 'do not use retired AI-901 study-resource wording',
      courses: ['ai-901'],
    ),
    RetiredTerm(
      pattern: 'Azure Bot Service',
      replacement: 'do not use retired AI-901 study-resource wording',
      courses: ['ai-901'],
    ),
    RetiredTerm(
      pattern: 'Form Recognizer',
      replacement: 'Azure Content Understanding in Foundry Tools',
      courses: ['ai-901'],
    ),
    RetiredTerm(
      pattern: 'Azure AI Document Intelligence',
      replacement: 'Azure Content Understanding in Foundry Tools',
      courses: ['ai-901'],
    ),
    RetiredTerm(
      pattern: 'Microsoft Cloud App Security',
      replacement: 'Microsoft Defender for Cloud Apps',
      courses: ['sc-900'],
    ),
    RetiredTerm(
      pattern: 'MCAS',
      replacement: 'Microsoft Defender for Cloud Apps',
      courses: ['sc-900'],
    ),
    RetiredTerm(
      pattern: 'Microsoft 365 Defender',
      replacement: 'Microsoft Defender XDR',
      courses: ['sc-900'],
    ),
    RetiredTerm(
      pattern: 'geo redundant zones',
      replacement: 'geo-zone-redundant storage (GZRS) under "redundancy options"',
      courses: allCourses,
    ),
    RetiredTerm(
      pattern: 'AI-900',
      replacement: 'AI-901',
      courses: allCourses,
    ),
    RetiredTerm(
      pattern: 'Azure AI Foundry',
      replacement: 'Microsoft Foundry / Foundry SDK',
      courses: ['ai-901'],
    ),
    RetiredTerm(
      pattern: 'Azure OpenAI',
      replacement: 'Microsoft Foundry / Foundry SDK',
      courses: ['ai-901'],
    ),
    RetiredTerm(
      pattern: 'Azure Speech service',
      replacement: 'Azure Speech in Foundry Tools',
      courses: ['ai-901'],
    ),
    RetiredTerm(
      pattern: 'Azure AI Speech',
      replacement: 'Azure Speech in Foundry Tools',
      courses: ['ai-901'],
    ),
    RetiredTerm(
      pattern: 'Azure AD B2B',
      replacement: 'external identities',
      courses: ['az-900'],
    ),
    RetiredTerm(
      pattern: 'Azure AD B2C',
      replacement: 'external identities',
      courses: ['az-900'],
    ),
    RetiredTerm(
      pattern: 'Azure AD Conditional Access',
      replacement: 'Microsoft Entra Conditional Access',
      courses: allCourses,
    ),
    RetiredTerm(
      pattern: 'regional pairs',
      replacement: 'region pairs',
      courses: ['az-900'],
    ),
    RetiredTerm(
      pattern: 'paired regions',
      replacement: 'region pairs',
      courses: ['az-900'],
    ),
    RetiredTerm(
      pattern: 'VM scale sets',
      replacement: 'Azure Virtual Machine Scale Sets',
      courses: ['az-900'],
    ),
    // Course-scoped retired/unverified wording.
    RetiredTerm(
      pattern: 'Service Trust Portal',
      replacement: 'Microsoft Service Trust Portal (SC-900 only; not AZ-900)',
      courses: ['az-900'],
    ),
  ];
}

/// A retired or non-exam wording pattern with its replacement and the courses
/// where the linter must enforce the rule.
class RetiredTerm {
  final String pattern;
  final String replacement;
  final List<String> courses;

  const RetiredTerm({
    required this.pattern,
    required this.replacement,
    required this.courses,
  });
}
