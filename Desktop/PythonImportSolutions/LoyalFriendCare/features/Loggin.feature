Feature: Kullanıcı Girişi

  Scenario: Başarılı Giriş
    Given LoyalFriendCare kullanıcısı login sayfasına gider
    When LoyalFriendCare kullanıcısı doğru bilgilerle siteye giriş yapar
    And Kullanıcı tarayıcıyı kapatır
