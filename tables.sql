-- Based on Trademark-Applications-Documentation-v2.0-07152005.pdf
DROP TABLE case_file_statements;
DROP TABLE trademarks CASCADE;
DROP TABLE case_file_event_statements ;
DROP TABLE prior_registration_applications ;
DROP TABLE foreign_applications;
DROP TABLE classifications;
DROP TABLE correspondent;
DROP TABLE case_file_owners;
DROP TABLE design_searches;
DROP TABLE international_registrations;
DROP TABLE madrid_international_filing_records CASCADE;
DROP TABLE madrid_history_events;

CREATE TABLE trademarks (
       -- file_segment                   varchar(4),                 -- Will always contain 'TMRK'
       action_key                        varchar(2),	             -- Action key for type of event
       -- Case file starts here
       serial_number                     varchar(8) PRIMARY KEY,     -- Case serial number (unique) -- DISPLAY
       registration_number               varchar(7),                 -- Registration no. -- DISPLAY
       transaction_date                  date,
       -- Case file header starts here
       filing_date                       date,                       -- DISPLAY
       registration_date                 date,                       -- DISPLAY
       status_code                       varchar(3),
       status_date                       date,
       mark_identification               text,                       -- DISPLAY
       mark_drawing_code                 varchar(4),
       published_for_opposition_date     date,                       -- DISPLAY
       amend_to_register_date            date, 
       abandonment_date                  date,
       cancellation_code                 varchar(1),
       cancellation_date                 date,
       republished_12c_date              date,
       domestic_rep_name                 text,
       attorney_docket_number            varchar(12),
       attorney_name                     text,                       -- Attorney of record
       -- Boolean fields indicating various statuses. All are either T
       -- or F. The _in stands for 'indicator'.
       principal_register_amended_in     varchar(1),     
       supplemental_register_amended_in  varchar(1),     
       trademark_in                      varchar(1),     
       collective_trademark_in           varchar(1),     
       service_mark_in                   varchar(1),     
       collective_service_mark_in        varchar(1),     
       collective_membership_mark_in     varchar(1),     
       certification_mark_in             varchar(1),     
       cancellation_pending_in           varchar(1),     
       published_concurrent_in           varchar(1),
       concurrent_use_in                 varchar(1),
       concurrent_use_proceeding_in      varchar(1),
       interference_pending_in           varchar(1),
       opposition_pending_in             varchar(1),
       section_12c_in                    varchar(1),
       section_2f_in                     varchar(1),
       section_2f_in_part_in             varchar(1),
       renewal_filed_in                  varchar(1),
       section_8_filed_in                 varchar(1),
       section_8_partial_accept_in        varchar(1),
       section_8_accepted_in              varchar(1),
       section_15_acknowledged_in         varchar(1),
       section_15_filed_in                varchar(1),
       supplemental_register_in          varchar(1),
       foreign_priority_in               varchar(1),
       change_registration_in             varchar(1),
       intent_to_use_in                  varchar(1),
       intent_to_use_current_in          varchar(1),
       filed_as_use_application_in       varchar(1),
       amended_to_use_application_in     varchar(1),
       use_application_currently_in      varchar(1),
       amended_to_itu_application_in     varchar(1),
       filing_basis_filed_as_44d_in      varchar(1),
       amended_to_44d_application_in     varchar(1),
       filing_basis_current_44d_in       varchar(1),
       filing_basis_filed_as_44e_in      varchar(1),
       amended_to_44e_application_in     varchar(1),
       filing_basis_current_44e_in       varchar(1),
       without_basis_currently_in        varchar(1),
       filing_current_no_basis_in        varchar(1),
       color_drawing_filed_in            varchar(1),
       color_drawing_currently_in        varchar(1),
       drawing_3d_filed_in               varchar(1),
       drawing_3d_current_in             varchar(1),
       standard_characters_claimed_in    varchar(1),
       filing_basis_filed_as_66a_in      varchar(1),
       filing_basis_current_66a_in       varchar(1),
       -- End of indicator fields
       renewal_date                      date,
       law_office_assigned_location_code varchar(3),
       current_location                  text,
       location_date                     date,
       employee_name                     text,
       -- Case file header ends here. Following are fields from other
       -- nodes that are unique to a given case
       other_related_in                  varchar(1)
);
        
        
CREATE TABLE case_file_statements (
       tm                                varchar(8) REFERENCES trademarks,
       type_code                         varchar(6),
       text                              text,
       PRIMARY KEY(tm, type_code)
);

CREATE TABLE case_file_event_statements (
       tm                                varchar(8) REFERENCES trademarks,
       code                              varchar(4),
       type                              varchar(1),                            
       description_text                  text,
       date                              date,
       number                            varchar(3),
       PRIMARY KEY(tm, code, date)
);

CREATE TABLE prior_registration_applications (
       tm                                varchar(8)  REFERENCES trademarks,
       relationship_type                 varchar(1),
       number                            varchar(8)
);

CREATE TABLE foreign_applications (
       tm                                varchar(8)  REFERENCES trademarks,
       filing_date                       date,
       registration_date                 date,
       registration_expiration_date      date,
       registration_renewal_date         date,
       registration_renewal_expiration_date date,
       entry_number                      varchar(3),
       application_number                varchar(12),
       country                           varchar(3),
       other                             varchar(3),
       registration_number               varchar(12),
       renewal_number                    varchar(12),
       foreign_priority_claim_in         varchar(1)
);     

CREATE TABLE classifications (
       tm                                varchar(8)  REFERENCES trademarks,
       international_code_total_no       varchar(2), 
       us_code_total_no                  varchar(2),                 
       international_code                varchar(3),
       us_code                           varchar(3),                          
       status_code                       varchar(1),                      
       status_date                       date,
       -- Although the following two are dates, they contain some
       -- placeholder values which cannot be represented as
       -- dates. Hence using varchar.
       first_use_anywhere_date           varchar(8),          -- DISPLAY
       first_use_in_commerce_date        varchar(8),          -- DISPLAY
       primary_code                      varchar(3)
);

CREATE TABLE correspondent (
       tm                               varchar(8)  REFERENCES trademarks,
       address_1                        text,
       address_2                        text,
       address_3                        text,  
       address_4                        text,
       address_5                        text
);

CREATE TABLE case_file_owners (
       tm                               varchar(8)  REFERENCES trademarks,
       entry_number                     varchar(2),
       party_type                       varchar(2),
       nationality_state                varchar(2),
       nationality_country              varchar(3),
       nationality_other                varchar(3),
       legal_entity_type_code           varchar(2),
       entity_statement                 text,
       party_name                       text,
       address_1                        text,
       address_2                        text,
       city                             text,
       state                            varchar(2),
       country                          varchar(2),
       other                            varchar(3),
       postcode                         varchar(15),
       dba_aka_text                     text,
       composed_of_statement            text,
       name_change_explanation          varchar(75)
);


CREATE TABLE design_searches (
       tm                               varchar(8)  REFERENCES trademarks,
       code                             varchar(6)
);


CREATE TABLE international_registrations (
       tm                                varchar(8)  REFERENCES trademarks,
       international_registration_number varchar(10),        -- DISPLAY
       international_registration_date   date,
       international_publication_date    date,
       international_renewal_date        date,
       auto_protection_date              date,
       international_death_date          date,
       international_status_code         varchar(3),
       international_status_date         date,
       priority_claimed_in               varchar(1),
       priority_claimed_date             date,
       first_refusal_in                  varchar(1)
);

CREATE TABLE madrid_international_filing_records (
       tm                                varchar (8) REFERENCES trademarks,
       reference_number                  varchar(20) PRIMARY KEY,
       entry_number                      varchar(3),
       original_filing_date_uspto        date,
       international_registration_number varchar(10),
       international_status_code         varchar(3),
       international_status_date         date,
       irregularity_reply_by_date        date,
       international_renewal_date        date
);

CREATE TABLE madrid_history_events (
       filing_record                     varchar(20) REFERENCES madrid_international_filing_records,
       code                              varchar(6),
       date                              date,
       description_text                  text,
       entry_number                      varchar(3),
       PRIMARY KEY (code, date, filing_record)
);

-- MISSING ITEMS
--  * ASSIGNMENT RECORDED
--  * Register


-- OTHERS TO BE INCLUDED
--  * Summarise case-file-statements
--  * Current filing basis/original filing basis    
--  * Summarise case-file-owner
--  * Summarise indicators to denote type of mark
