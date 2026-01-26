// testData.js - Test verilerini yöneten sınıf

class TestData {
  constructor() {
    // API konfigürasyonları
    this.apiConfig = {
      base_url: Cypress.config('baseUrl') || 'https://qa.instulearn.com',
      adminEmail: Cypress.env('adminEmail') || '162.admin@instulearn.com',
      adminPassword: Cypress.env('adminPassword') || '162162162',
      invalidToken: Cypress.env('invalidToken') || 'invalid_token',
      xApiKey: '1234'
    };

    // Test verileri
    this.testUsers = {
      admin: {
        email: this.apiConfig.adminEmail,
        password: this.apiConfig.adminPassword
      },
      invalid: {
        email: 'invalid@instulearn.com',
        password: 'wrongpassword'
      }
    };

    // API endpoints
    this.endpoints = {
      token: '/api/token',
      courses: '/api/courses',
      departments: '/api/departments',
      support: '/api/addSupport'
    };

    // Test verileri - Course örnekleri
    this.testCourses = {
      validCourse: {
        name: 'Test Course',
        duration: 30,
        description: 'A test course for API testing'
      },
      updatedCourse: {
        name: 'Updated Test Course',
        duration: 45,
        description: 'Updated course description'
      }
    };

    // Department test verileri
    this.testDepartments = {
      validDepartment: {
        name: 'Test Department',
        description: 'A test department'
      }
    };
  }

  // API config getter
  getApiConfig(key) {
    return this.apiConfig[key];
  }

  // Test user getter
  getTestUser(userType = 'admin') {
    return this.testUsers[userType];
  }

  // Endpoint getter
  getEndpoint(key) {
    return this.endpoints[key];
  }

  // Test data getter
  getTestCourse(courseType = 'validCourse') {
    return this.testCourses[courseType];
  }

  getTestDepartment(deptType = 'validDepartment') {
    return this.testDepartments[deptType];
  }

  // Dinamik test verisi oluşturma
  generateRandomCourse() {
    const randomId = Math.floor(Math.random() * 10000);
    return {
      name: `Random Course ${randomId}`,
      duration: Math.floor(Math.random() * 100) + 10,
      description: `Random course description ${randomId}`
    };
  }

  generateRandomDepartment() {
    const randomId = Math.floor(Math.random() * 10000);
    return {
      name: `Random Department ${randomId}`,
      description: `Random department description ${randomId}`
    };
  }

  // Config güncelleme (çalışma zamanında)
  updateApiConfig(key, value) {
    this.apiConfig[key] = value;
  }

  updateTestUser(userType, userData) {
    this.testUsers[userType] = { ...this.testUsers[userType], ...userData };
  }
}

// Singleton instance
const testData = new TestData();

export default testData;