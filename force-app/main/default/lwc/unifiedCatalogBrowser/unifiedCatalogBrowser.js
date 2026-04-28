import { LightningElement, wire } from 'lwc';

export default class UnifiedCatalogBrowser extends LightningElement {
    catalogData = null;
    selectedEntity = null;
    isLoading = true;
    error = null;

    catalogEntities = [
        {
            entity_name: 'Account',
            source_system: 'Salesforce',
            type: 'core_object',
            fieldCount: 6,
            description: 'Customer account information'
        },
        {
            entity_name: 'Contact',
            source_system: 'Salesforce',
            type: 'core_object',
            fieldCount: 7,
            description: 'Contact records and details'
        },
        {
            entity_name: 'Opportunity',
            source_system: 'Salesforce',
            type: 'core_object',
            fieldCount: 5,
            description: 'Sales opportunities and pipeline'
        },
        {
            entity_name: 'Policy',
            source_system: 'External System',
            type: 'external_object',
            fieldCount: 8,
            description: 'Insurance policy information'
        }
    ];

    connectedCallback() {
        setTimeout(() => {
            this.isLoading = false;
            this.catalogData = this.catalogEntities;
        }, 500);
    }

    handleBack() {
        this.selectedEntity = null;
    }

    get hasEntities() {
        return this.catalogData && this.catalogData.length > 0;
    }
}
