// apiHelpers.js - API test yardımcı fonksiyonları
import testData from './testData';

class ApiHelpers {
  constructor() {
    this.baseUrl = testData.getApiConfig('base_url');
    this.token = null;
    this.id = 0; // Path param için
  }

  // Authentication - Token üretme
  generateToken() {
    const adminUser = testData.getTestUser('admin');

    return cy.request({
      method: 'POST',
      url: `${this.baseUrl}${testData.getEndpoint('token')}`,
      headers: {
        'Accept': 'application/json',
        'x-api-key': testData.getApiConfig('xApiKey'),
        'Content-Type': 'application/json'
      },
      body: {
        email: adminUser.email,
        password: adminUser.password
      }
    }).then((response) => {
      expect(response.status).to.eq(200);
      this.token = response.body.data.access_token;
      cy.log('Token generated: ' + this.token);
      return this.token;
    });
  }

  // Request spec ayarlama (HooksAPI benzeri)
  setUpApi(userType = 'admin') {
    if (userType === 'admin') {
      return this.generateToken().then(() => {
        // Cypress'te global headers ayarlama
        cy.window().then((win) => {
          // Veya cy.intercept ile headers ekle
        });
      });
    } else {
      this.token = testData.getApiConfig('invalidToken');
    }
  }

  // Path parametre işleme (API_Methods.pathParam benzeri)
  buildPath(rawPaths) {
    let fullPath = rawPaths;
    let id = 0;

    // Basit path param parsing - {id} gibi
    const pathParamRegex = /\{(\w+)\}/g;
    let match;
    while ((match = pathParamRegex.exec(rawPaths)) !== null) {
      const param = match[1];
      if (param === 'id') {
        // ID'yi çıkar (örnek: /api/courses/{id} -> /api/courses/123)
        // Gerçek kullanımda dinamik ID geçin
        fullPath = fullPath.replace(match[0], id.toString());
      }
    }

    cy.log('Built path: ' + fullPath);
    return fullPath;
  }

  // Genel request gönderme (API_Methods.sendRequest benzeri)
  sendRequest(httpMethod, endpoint, requestBody = null) {
    const headers = {
      'Accept': 'application/json',
      'x-api-key': testData.getApiConfig('xApiKey')
    };

    if (this.token) {
      headers['Authorization'] = `Bearer ${this.token}`;
    }

    if (requestBody && (httpMethod === 'POST' || httpMethod === 'PATCH' || httpMethod === 'PUT')) {
      headers['Content-Type'] = 'application/json';
    }

    return cy.request({
      method: httpMethod,
      url: `${this.baseUrl}${endpoint}`,
      headers: headers,
      body: requestBody,
      failOnStatusCode: false // Exception handling için
    }).then((response) => {
      cy.log(`${httpMethod} ${endpoint} -> ${response.status}`);
      if (response.body) {
        cy.log('Response body: ' + JSON.stringify(response.body));
      }
      return response;
    });
  }

  // HTTP method'lar
  get(endpoint) {
    return this.sendRequest('GET', endpoint);
  }

  post(endpoint, body) {
    return this.sendRequest('POST', endpoint, body);
  }

  patch(endpoint, body) {
    return this.sendRequest('PATCH', endpoint, body);
  }

  delete(endpoint) {
    return this.sendRequest('DELETE', endpoint);
  }

  // Assertions (API_Methods.statusCodeAssert, assertBody benzeri)
  assertStatusCode(response, expectedStatus) {
    expect(response.status).to.eq(expectedStatus);
  }

  assertBody(response, path, expectedValue) {
    const actualValue = Cypress._.get(response.body, path);
    expect(actualValue).to.eq(expectedValue);
  }

  // JSON Path ile assertion
  assertJsonPath(response, jsonPath, expectedValue) {
    // Basit implementation - lodash get ile
    const actualValue = Cypress._.get(response.body, jsonPath.replace(/^\$\./, ''));
    expect(actualValue).to.eq(expectedValue);
  }

  // Department ID keşfi (ApiStepsBase.collectValidDepartmentIds benzeri)
  collectValidDepartmentIds() {
    const endpoints = [
      testData.getEndpoint('departments'),
      '/api/support/departments',
      '/departments'
    ];

    const ids = new Set();

    endpoints.forEach(endpoint => {
      this.get(endpoint).then(response => {
        if (response.status === 200 && response.body) {
          // Array ise
          if (Array.isArray(response.body)) {
            response.body.forEach(item => {
              if (item.id) ids.add(item.id);
            });
          }
          // data altında array ise
          if (response.body.data && Array.isArray(response.body.data)) {
            response.body.data.forEach(item => {
              if (item.id) ids.add(item.id);
            });
          }
        }
      });
    });

    return Array.from(ids);
  }

  // POST türleri (ApiStepsBase.postJson, postForm benzeri)
  postJson(endpoint, jsonBody) {
    return cy.request({
      method: 'POST',
      url: `${this.baseUrl}${endpoint}`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': this.token ? `Bearer ${this.token}` : undefined,
        'x-api-key': testData.getApiConfig('xApiKey')
      },
      body: jsonBody
    });
  }

  postForm(endpoint, formData) {
    const formBody = new URLSearchParams();
    Object.keys(formData).forEach(key => {
      formBody.append(key, formData[key]);
    });

    return cy.request({
      method: 'POST',
      url: `${this.baseUrl}${endpoint}`,
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Authorization': this.token ? `Bearer ${this.token}` : undefined,
        'x-api-key': testData.getApiConfig('xApiKey')
      },
      body: formBody.toString()
    });
  }

  // Try-catch request (API_Methods.tryCatchRequest benzeri)
  tryCatchRequest(httpMethod, endpoint, requestBody = null) {
    return this.sendRequest(httpMethod, endpoint, requestBody).then(response => {
      return response;
    }).catch(error => {
      cy.log('Request failed: ' + error.message);
      return error.message;
    });
  }

  // DataTable assertion (ApiStepsBase.assertDataTable benzeri)
  assertDataTable(response, dataTable) {
    dataTable.forEach(row => {
      const path = row.path;
      const expectedValue = row.value;
      this.assertJsonPath(response, path, expectedValue);
    });
  }
}

// Singleton instance
const apiHelpers = new ApiHelpers();

export default apiHelpers;