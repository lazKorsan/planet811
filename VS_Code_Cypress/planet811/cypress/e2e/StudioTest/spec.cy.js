import apiHelpers from '../../support/apiHelpers';

describe('API Tests - Courses', () => {
  before(() => {
    // Admin olarak giriş yap
    apiHelpers.setUpApi('admin');
  });

  it('should get all courses successfully', () => {
    apiHelpers.get('/api/courses').then((response) => {
      // Status code kontrolü
      apiHelpers.assertStatusCode(response, 200);

      // Response body kontrolü
      expect(response.body).to.be.an('object');

      // Eğer courses array'i varsa kontrol et
      if (response.body.courses) {
        expect(response.body.courses).to.be.an('array');
        cy.log('Courses count: ' + response.body.courses.length);
      }

      // Response pretty print
      cy.log('Response: ' + JSON.stringify(response.body, null, 2));
    });
  });

  it('should get courses with direct cy.request', () => {
    // Önce token al
    apiHelpers.generateToken().then(() => {
      cy.request({
        method: 'GET',
        url: '/api/courses',
        headers: {
          'Authorization': `Bearer ${apiHelpers.token}`,
          'Accept': 'application/json',
          'x-api-key': '1234'
        }
      }).then((response) => {
        expect(response.status).to.eq(200);
        cy.log('Direct GET successful');
        cy.log('Courses response: ' + JSON.stringify(response.body, null, 2));
      });
    });
  });
});