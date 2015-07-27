/*!
 * @author:    Divio AG
 * @copyright: http://www.divio.ch
 */

'use strict';
/* global element, by, browser, expect */

// #############################################################################
// INTEGRATION TEST PAGE OBJECT

var jobsPage = {
    site: 'http://127.0.0.1:8000/en/',
    mainElementsWaitTime: 12000,
    iframeWaitTime: 15000,

    // log in
    editModeLink: element(by.css('.inner a[href="/?edit"]')),
    usernameInput: element(by.id('id_cms-username')),
    passwordInput: element(by.id('id_cms-password')),
    loginButton: element(by.css('.cms_form-login input[type="submit"]')),
    userMenus: element.all(by.css('.cms_toolbar-item-navigation > li > a')),
    testLink: element(by.css('.selected a')),

    cmsLogin: function (credentials) {
        // object can contain username and password, if not set it will
        // fallback to 'admin'
        credentials = credentials ||
            { username: 'admin', password: 'admin' };

        jobsPage.usernameInput.clear();

        // fill in email field
        jobsPage.usernameInput.sendKeys(
            credentials.username).then(function () {
            jobsPage.passwordInput.clear();

            // fill in password field
            return jobsPage.passwordInput.sendKeys(
                credentials.password);
        }).then(function () {
            jobsPage.loginButton.click();

            // wait for user menu to appear
            browser.wait(browser.isElementPresent(
                jobsPage.userMenus.first()),
                jobsPage.mainElementsWaitTime);

            // validate user menu
            expect(jobsPage.userMenus.first().isDisplayed())
                .toBeTruthy();
        });
    }

};

module.exports = jobsPage;