// https://docs.cypress.io/api/introduction/api.html

describe("ManageAlerts.vue", () => {
  it("Visits Manage Alerts", () => {
    cy.visit("/");
    cy.get('div[name="AlertsTable"]').should('be.visible');
  });
});
