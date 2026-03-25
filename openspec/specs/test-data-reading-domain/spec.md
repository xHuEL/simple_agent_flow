## ADDED Requirements

### Requirement: Reading Domain Test Data Generation
The system SHALL provide test data specifically designed for reading domain applications, containing author names and book titles.

#### Scenario: CSV format test data generation
- **WHEN** the test data is generated in CSV format
- **THEN** it MUST contain 30 unique author-book title combinations
- **AND** the data MUST follow the format: slotName,slotReName,slotType
- **AND** slotName SHALL contain author names
- **AND** slotReName SHALL contain book titles in snake_case format
- **AND** slotType SHALL be "string" for all entries

#### Scenario: TSV format test data generation  
- **WHEN** the test data is generated in TSV format
- **THEN** it MUST contain 30 unique author-book title combinations
- **AND** the data MUST use tab separation instead of commas
- **AND** all other format requirements SHALL be maintained

#### Scenario: Data diversity and quality
- **WHEN** examining the generated test data
- **THEN** it MUST include authors from different literary periods
- **AND** it MUST include both Chinese and international authors
- **AND** it MUST include various literary genres
- **AND** book titles SHALL be real and recognizable works
- **AND** author names SHALL be accurately formatted

#### Scenario: Format compatibility
- **WHEN** using the new test data with existing data insertion tools
- **THEN** it MUST be parsable by the existing CSV/TSV parsers
- **AND** it MUST pass all existing data validation rules
- **AND** it MUST be insertable into Elasticsearch without errors

#### Scenario: Special character handling
- **WHEN** test data contains special characters in book titles or author names
- **THEN** the data MUST be properly encoded in UTF-8
- **AND** special characters SHALL be preserved during parsing and insertion
- **AND** the data MUST not cause parsing errors due to special characters