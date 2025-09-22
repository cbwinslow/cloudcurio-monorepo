# Neo4j Knowledge Graph Schema for OSINT Data

## Node Types

### Person
- id (UUID)
- name (string)
- username (string)
- email (string)
- phone (string)
- bio (string)
- profile_image_url (string)
- created_at (datetime)
- updated_at (datetime)

### Email
- id (UUID)
- address (string)
- is_valid (boolean)
- is_disposable (boolean)
- created_at (datetime)
- updated_at (datetime)

### Domain
- id (UUID)
- name (string)
- registrar (string)
- creation_date (datetime)
- expiration_date (datetime)
- status (string)
- created_at (datetime)
- updated_at (datetime)

### IPAddress
- id (UUID)
- address (string)
- version (string)  // IPv4 or IPv6
- hostname (string)
- location (point)  // Geo coordinates
- isp (string)
- organization (string)
- created_at (datetime)
- updated_at (datetime)

### SocialProfile
- id (UUID)
- platform (string)  // twitter, facebook, linkedin, etc.
- profile_id (string)
- username (string)
- url (string)
- created_at (datetime)
- updated_at (datetime)

### PhoneNumber
- id (UUID)
- number (string)
- country_code (string)
- is_valid (boolean)
- type (string)  // mobile, landline, voip
- created_at (datetime)
- updated_at (datetime)

### Organization
- id (UUID)
- name (string)
- description (string)
- industry (string)
- website (string)
- founded (datetime)
- created_at (datetime)
- updated_at (datetime)

## Relationship Types

### EMAIL_ASSOCIATED_WITH
- from: Email
- to: Person
- confidence (float)

### DOMAIN_REGISTERED_BY
- from: Domain
- to: Person/Organization
- confidence (float)

### IP_RESOLVES_TO
- from: IPAddress
- to: Domain
- confidence (float)

### PERSON_HAS_SOCIAL_PROFILE
- from: Person
- to: SocialProfile
- confidence (float)

### PERSON_HAS_PHONE
- from: Person
- to: PhoneNumber
- confidence (float)

### ORGANIZATION_EMPLOYS
- from: Organization
- to: Person
- title (string)
- department (string)
- start_date (datetime)
- end_date (datetime)
- confidence (float)

### DOMAIN_HOSTED_ON
- from: Domain
- to: IPAddress
- confidence (float)

### IP_CONNECTED_TO
- from: IPAddress
- to: IPAddress
- connection_type (string)
- confidence (float)

### PERSON_ASSOCIATED_WITH
- from: Person
- to: Person
- relationship_type (string)  // friend, colleague, family
- confidence (float)

## Indexes

1. CREATE INDEX ON :Person(username)
2. CREATE INDEX ON :Person(email)
3. CREATE INDEX ON :Email(address)
4. CREATE INDEX ON :Domain(name)
5. CREATE INDEX ON :IPAddress(address)
6. CREATE INDEX ON :SocialProfile(platform, username)
7. CREATE INDEX ON :PhoneNumber(number)
8. CREATE INDEX ON :Organization(name)

## Constraints

1. CREATE CONSTRAINT ON (p:Person) ASSERT p.id IS UNIQUE
2. CREATE CONSTRAINT ON (e:Email) ASSERT e.address IS UNIQUE
3. CREATE CONSTRAINT ON (d:Domain) ASSERT d.name IS UNIQUE
4. CREATE CONSTRAINT ON (ip:IPAddress) ASSERT ip.address IS UNIQUE
5. CREATE CONSTRAINT ON (sp:SocialProfile) ASSERT sp.profile_id IS UNIQUE
6. CREATE CONSTRAINT ON (pn:PhoneNumber) ASSERT pn.number IS UNIQUE
7. CREATE CONSTRAINT ON (o:Organization) ASSERT o.name IS UNIQUE