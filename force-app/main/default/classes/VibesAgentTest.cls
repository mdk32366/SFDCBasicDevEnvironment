@isTest
private class VibesAgentTest {
    
    @isTest
    static void testProcessVibes() {
        String result = VibesAgent.processVibes('test input');
        System.assertEquals('Processed: test input', result);
    }
    
    @isTest
    static void testHealthCheck() {
        Map<String, Object> health = VibesAgent.healthCheck();
        System.assertEquals('healthy', health.get('status'));
        System.assertEquals('VibesAgent', health.get('agent'));
    }
}
