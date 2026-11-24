<template>
  <main class="min-h-screen bg-[#f8f7fc] px-3 py-3 text-[#25213a] sm:px-5 lg:px-8">
    <header
      class="dashboard-topbar sticky top-0 z-30 -mx-3 -mt-3 mb-4 border-b border-[#e9e5f1] bg-white/95 px-3 py-2 shadow-sm backdrop-blur sm:-mx-5 sm:px-5 lg:-mx-8 lg:px-8">
      <div class="flex min-h-10 items-center gap-2 sm:gap-3">
        <div class="relative shrink-0">
          <button type="button"
            class="flex min-h-10 items-center gap-2 rounded-lg border border-[#e9e5f1] bg-white px-2.5 text-left hover:border-[#c9bddf] sm:px-3"
            aria-haspopup="menu" :aria-expanded="workspaceMenuOpen" @click="workspaceMenuOpen = !workspaceMenuOpen">
            <span class="grid h-8 w-8 place-items-center rounded-lg bg-gradient-to-br from-[#453D89] to-[#C8499A] text-white">
              <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
                stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
                aria-hidden="true">
                <rect x="3" y="3" width="7" height="7" rx="1" />
                <rect x="14" y="3" width="7" height="7" rx="1" />
                <rect x="3" y="14" width="7" height="7" rx="1" />
                <rect x="14" y="14" width="7" height="7" rx="1" />
              </svg>
            </span>
            <span class="hidden min-w-0 sm:block">
              <span class="block truncate text-xs font-bold text-[#25213a]">HR Setup</span>
              <span class="block truncate text-[10px] text-gray-500">Frappe HR</span>
            </span>
            <svg class="hidden text-gray-500 sm:block" xmlns="http://www.w3.org/2000/svg" width="14" height="14"
              viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" aria-hidden="true">
              <path d="m6 9 6 6 6-6" />
            </svg>
          </button>

          <div v-if="workspaceMenuOpen"
            class="absolute left-0 top-full z-50 mt-2 w-60 rounded-xl border border-[#e9e5f1] bg-white p-2 shadow-xl"
            role="menu">
            <p class="px-3 py-2 text-[10px] font-bold uppercase tracking-wider text-gray-500">{{ t("HRMS workspace") }}</p>
            <button v-for="item in workspaceMenuItems" :key="item.href" type="button"
              class="w-full rounded-lg px-3 py-2 text-left text-xs font-semibold hover:bg-purple-50"
              role="menuitem" @click="openWorkspaceRoute(item.href)">{{ t(item.label) }}</button>
            <p v-if="!workspaceMenuItems.length" class="px-3 py-2 text-xs text-gray-500">
              {{ t("No HRMS navigation links are available.") }}
            </p>
          </div>
        </div>

        <button type="button"
          class="hidden h-10 min-w-0 flex-1 items-center justify-between gap-3 rounded-lg border border-[#e9e5f1] bg-[#faf9fd] px-3 text-left text-xs text-gray-500 hover:border-[#c9bddf] sm:flex"
          :aria-label="t('Open HRMS search')" @click="openGlobalSearch">
          <span class="flex min-w-0 items-center gap-2 truncate">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
              aria-hidden="true">
              <circle cx="11" cy="11" r="7" />
              <path d="m20 20-4-4" />
            </svg>
            {{ t("Search employees, records...") }}
          </span>
          <kbd class="shrink-0 rounded border border-[#e9e5f1] bg-white px-1.5 py-0.5 text-[10px]">Ctrl+K</kbd>
        </button>
        <button type="button"
          class="grid h-10 w-10 shrink-0 place-items-center rounded-lg border border-[#e9e5f1] text-[#625c70] hover:bg-purple-50 hover:text-[#453D89] sm:hidden"
          :aria-label="t('Open HRMS search')" @click="openGlobalSearch">
          <svg xmlns="http://www.w3.org/2000/svg" width="18" height="18" viewBox="0 0 24 24" fill="none"
            stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
            aria-hidden="true">
            <circle cx="11" cy="11" r="7" />
            <path d="m20 20-4-4" />
          </svg>
        </button>

        <div ref="languagePicker" class="relative flex shrink-0 items-center gap-1.5" @pointerdown.stop>
          <label for="dashboard-language" class="sr-only sm:not-sr-only text-[10px] font-semibold text-gray-600">
            {{ t("Language") }}
          </label>
          <button id="dashboard-language" ref="languagePickerButton" type="button" :disabled="languageSaving"
            :aria-label="t('Language')" aria-haspopup="listbox" :aria-expanded="languagePickerOpen"
            aria-controls="dashboard-language-options"
            class="flex h-9 w-24 items-center justify-between gap-1 rounded-md border border-[#e9e5f1] bg-white px-2 text-[10px] text-[#25213a] disabled:opacity-60 sm:w-32 sm:text-xs"
            @click="toggleLanguagePicker">
            <span class="truncate">{{ selectedLanguageLabel }}</span>
            <svg class="shrink-0 text-gray-500" xmlns="http://www.w3.org/2000/svg" width="12" height="12"
              viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" aria-hidden="true">
              <path d="m6 9 6 6 6-6" />
            </svg>
          </button>
          <div v-if="languagePickerOpen"
            class="absolute right-0 top-full z-50 mt-2 w-56 overflow-hidden rounded-xl border border-[#e9e5f1] bg-white shadow-xl sm:w-64">
            <div class="border-b border-[#eeeaf5] p-2">
              <input ref="languageSearchInput" v-model="languageSearch" type="search"
                :aria-label="t('Search languages')" :placeholder="t('Search languages...')"
                class="h-9 w-full rounded-md border border-[#e9e5f1] px-3 text-xs text-[#25213a] outline-none focus:border-[#453D89]"
                @keydown.esc="closeLanguagePicker(true)" />
            </div>
            <div id="dashboard-language-options" class="max-h-60 overflow-y-auto p-1" role="listbox"
              :aria-label="t('Languages')">
              <button v-for="language in filteredLanguages" :key="language.value" type="button" role="option"
                :aria-selected="language.value === selectedLanguage"
                class="block w-full truncate rounded-md px-3 py-2 text-left text-xs hover:bg-purple-50"
                :class="language.value === selectedLanguage ? 'bg-purple-50 font-semibold text-[#453D89]' : 'text-[#25213a]'"
                @click="selectLanguage(language.value)">
                {{ language.label }}
              </button>
              <p v-if="!filteredLanguages.length" class="px-3 py-3 text-xs text-gray-500">
                {{ t("No languages found.") }}
              </p>
            </div>
          </div>
        </div>

        <div class="relative shrink-0">
          <button type="button"
            class="relative grid h-10 w-10 place-items-center rounded-lg text-[#625c70] hover:bg-purple-50 hover:text-[#453D89]"
            :aria-label="t('Notifications')" :aria-expanded="notificationsOpen" @click="toggleNotifications">
            <svg xmlns="http://www.w3.org/2000/svg" width="19" height="19" viewBox="0 0 24 24" fill="none"
              stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"
              aria-hidden="true">
              <path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" />
              <path d="M10 21h4" />
            </svg>
            <span v-if="unreadCount"
              class="absolute right-0.5 top-0.5 grid min-h-4 min-w-4 place-items-center rounded-full bg-[#C8499A] px-1 text-[9px] font-bold text-white">
              {{ unreadCount > 99 ? "99+" : unreadCount }}
            </span>
          </button>
          <section v-if="notificationsOpen"
            class="absolute right-0 top-full z-50 mt-2 w-80 max-w-[calc(100vw-2rem)] overflow-hidden rounded-xl border border-[#e9e5f1] bg-white shadow-xl"
            :aria-label="t('Notifications')">
            <div class="flex items-center justify-between border-b border-[#eeeaf5] px-4 py-3">
              <h2 class="text-sm font-bold">{{ t("Notifications") }}</h2>
              <button v-if="unreadCount" type="button" class="text-[10px] font-bold text-[#453D89]"
                @click="markAllNotificationsRead">{{ t("Mark all read") }}</button>
            </div>
            <div class="max-h-80 overflow-y-auto">
              <p v-if="notificationsLoading" class="p-4 text-xs text-gray-500">{{ t("Loading notifications...") }}</p>
              <p v-else-if="!notifications.length" class="p-4 text-xs text-gray-500">{{ t("No notifications to show.") }}</p>
              <button v-for="notification in notifications" :key="notification.name" type="button"
                class="block w-full border-b border-[#f2eff7] px-4 py-3 text-left last:border-0 hover:bg-[#faf9fd]"
                @click="openNotification(notification)">
                <span class="flex items-start gap-2">
                  <span class="mt-1.5 h-2 w-2 shrink-0 rounded-full"
                    :class="isRead(notification) ? 'bg-gray-200' : 'bg-[#C8499A]'"></span>
                  <span class="min-w-0">
                    <strong class="block truncate text-xs">{{ notification.subject || t("Notification") }}</strong>
                    <span class="mt-1 block text-[10px] leading-4 text-gray-600">{{ notificationMessage(notification) }}</span>
                    <span class="mt-1 block text-[9px] text-gray-400">{{ notification.creation }}</span>
                  </span>
                </span>
              </button>
            </div>
          </section>
        </div>

        <div class="relative shrink-0">
          <button type="button"
            class="flex min-w-0 items-center gap-2 rounded-lg px-1.5 py-1 hover:bg-purple-50"
            :aria-label="t('Administrator menu')" aria-haspopup="menu" :aria-expanded="profileMenuOpen"
            @click="profileMenuOpen = !profileMenuOpen">
            <span class="grid h-8 w-8 shrink-0 place-items-center overflow-hidden rounded-full bg-[#faf4fc] text-[10px] font-bold text-[#453D89]">
              <img v-if="userImage" :src="userImage" :alt="profileDisplayName" class="h-full w-full object-cover"
                @error="userImage = ''" />
              <span v-else>{{ profileInitials }}</span>
            </span>
            <span class="hidden max-w-24 truncate text-xs font-semibold sm:block">{{ profileDisplayName }}</span>
            <svg class="hidden text-gray-500 sm:block" xmlns="http://www.w3.org/2000/svg" width="14" height="14"
              viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
              stroke-linejoin="round" aria-hidden="true">
              <path d="m6 9 6 6 6-6" />
            </svg>
          </button>
          <div v-if="profileMenuOpen"
            class="absolute right-0 top-full z-50 mt-2 w-60 rounded-xl border border-[#e9e5f1] bg-white p-2 shadow-xl"
            role="menu" :aria-label="t('Administrator options')">
            <div class="border-b border-[#eeeaf5] px-3 py-2">
              <p class="truncate text-xs font-bold text-[#25213a]">{{ profileDisplayName }}</p>
              <p class="mt-1 truncate text-[10px] text-gray-500">{{ loggedUser }}</p>
            </div>
            <p v-if="languageSaving" class="px-3 py-2 text-[10px] text-gray-500">{{ t("Saving language...") }}</p>
            <p v-if="languageError" class="px-3 py-2 text-[10px] text-red-600" role="alert">{{ languageError }}</p>
            <button type="button"
              class="w-full rounded-lg px-3 py-2.5 text-left text-xs font-semibold text-[#453D89] hover:bg-purple-50"
              role="menuitem" @click="openUserProfile">{{ t("Profile") }}</button>
            <button type="button"
              class="w-full rounded-lg px-3 py-2.5 text-left text-xs font-semibold text-[#453D89] hover:bg-purple-50"
              role="menuitem" @click="openHrSettings">{{ t("Settings") }}</button>
            <button type="button"
              class="w-full rounded-lg px-3 py-2.5 text-left text-xs font-semibold text-red-600 hover:bg-red-50"
              role="menuitem" @click="signOut">{{ t("Sign out") }}</button>
          </div>
        </div>

        <button v-if="!isEmployee" type="button"
          class="hidden shrink-0 items-center gap-1.5 rounded-lg bg-gradient-to-r from-[#453D89] to-[#C8499A] px-3 py-2 text-xs font-bold text-white shadow-sm hover:brightness-105 sm:flex"
          @click="createEmployee">
          <span class="text-base leading-none">+</span>
          {{ t("New Employee") }}
        </button>
      </div>
    </header>

    <!-- HERO -->
    <section
      class="relative overflow-hidden rounded-2xl bg-gradient-to-r from-[#453D89] to-[#C8499A] p-5 text-white shadow-md sm:p-6">
      <div class="pointer-events-none absolute -right-8 -top-12 h-40 w-40 rounded-full bg-white/10"></div>

      <div class="relative grid items-center gap-5 lg:grid-cols-[1.2fr_0.8fr]">
        <div>
          <span
            class="inline-flex items-center gap-2 rounded-full border border-white/20 bg-white/10 px-3 py-1.5 text-[9px] font-bold tracking-widest">
            <span class="h-2 w-2 rounded-full bg-emerald-300"></span>{{ roleLabel }}
          </span>

          <h1 class="mt-3 text-2xl font-black leading-tight sm:text-3xl">
            {{ t("Good") }} {{ greeting }} <span class="text-[#FFD8EF]">{{ displayName }}</span>
          </h1>

          <!-- <p class="mt-2 max-w-xl text-xs leading-5 text-white/80 sm:text-sm">
            Good {{ greeting }}, {{ displayName }}.
          </p> -->

          <div class="mt-4 flex flex-wrap gap-2">
            <button class="rounded-lg bg-white px-4 py-2.5 text-xs font-extrabold text-[#453D89]"
              @click="openRoute(isEmployee ? '/app/attendance' : '/app/employee')">
              {{ t(isEmployee ? "My Attendance" : "Employee Directory") }} ↗
            </button>
            <button class="rounded-lg border border-white/30 bg-white/10 px-4 py-2.5 text-xs font-bold text-white"
              @click="openRoute('/app/leave-application')">
              {{ t(isEmployee ? "Request Leave" : "Leave Applications") }} ↗
            </button>
          </div>
        </div>

        <div class="flex items-center gap-3 rounded-xl border border-white/30 bg-white/95 p-4 text-[#25213a] shadow">
          <div
            class="grid h-14 w-14 shrink-0 place-items-center overflow-hidden rounded-xl bg-gradient-to-br from-[#453D89] to-[#C8499A] text-xl font-black text-white">
            <img v-if="userImage" :src="userImage" :alt="displayName" class="h-full w-full object-cover"
              @error="userImage = ''" />
            <span v-else>{{ initials }}</span>
          </div>
          <div class="min-w-0 flex-1">
            <p class="text-[9px] font-bold uppercase tracking-widest text-[#C8499A]">{{ t("Welcome back") }}</p>
            <h2 class="mt-1 truncate text-base font-black">{{ displayName }}</h2>
            <p class="mt-1 truncate text-xs text-gray-500">{{ employee.designation || roleDisplay }}</p>
            <p class="mt-1 truncate text-[10px] text-gray-600">{{ employee.name || loggedUser }}</p>
          </div>
          <button class="shrink-0 text-xs font-bold text-[#C8499A]" @click="openRoute('/app/user')">{{ t("Profile") }} ↗</button>
        </div>
      </div>

      <div
        class="relative mt-4 flex flex-wrap justify-between gap-2 border-t border-white/20 pt-3 text-[10px] text-white/75">
        <span>{{ todayLabel }}</span>
        <span>{{ roleDisplay }}</span>
      </div>
    </section>

    <!-- LOADING -->
    <div v-if="loading"
      class="mt-4 flex items-center gap-3 rounded-xl border border-purple-100 bg-white p-3 text-sm font-semibold text-[#453D89]">
      <span class="h-4 w-4 animate-spin rounded-full border-2 border-purple-200 border-t-[#453D89]"></span>
      {{ t("Loading dashboard...") }}
    </div>

    <!-- ERROR -->
    <div v-if="errorMessage"
      class="mt-4 flex flex-wrap items-center justify-between gap-3 rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-700"
      role="alert">
      <span>{{ errorMessage }}</span>
      <button class="rounded-lg bg-gradient-to-r from-[#453D89] to-[#C8499A] px-3 py-2 text-xs font-bold text-white"
        @click="loadDashboard">{{ t("Retry") }}</button>
    </div>

    <!-- GLOBAL DATE RANGE FILTER -->

    <section class="mt-3 rounded-xl border border-[#eeeaf5] bg-white px-4 py-3 shadow-sm">
      <div class="flex flex-wrap items-center gap-3">

        <!-- Title -->
        <div class="mr-auto min-w-fit">
          <h2 class="text-sm font-black text-[#25213a]">
            {{ t("Dashboard Date Filter") }}
          </h2>
          <p class="text-[10px] text-gray-600">
            {{ t(filterApplied ? "Custom date range" : "Default: Today") }}
          </p>
        </div>

        <!-- Start Date -->
        <div class="flex items-center gap-2">
          <label for="dashboard-start-date" class="whitespace-nowrap text-xs font-bold text-gray-600">
            {{ t("From") }}
          </label>
          <input id="dashboard-start-date" v-model="startDate" type="date"
            class="h-9 w-[145px] rounded-lg border border-purple-100 bg-[#faf9fd] px-2 text-xs font-semibold text-[#453D89] outline-none focus:border-[#C8499A]" />
        </div>

        <!-- End Date -->
        <div class="flex items-center gap-2">
          <label for="dashboard-end-date" class="whitespace-nowrap text-xs font-bold text-gray-600">
            {{ t("To") }}
          </label>
          <input id="dashboard-end-date" v-model="endDate" type="date"
            class="h-9 w-[145px] rounded-lg border border-purple-100 bg-[#faf9fd] px-2 text-xs font-semibold text-[#453D89] outline-none focus:border-[#C8499A]" />
        </div>

        <!-- Apply -->
        <button
          class="h-9 whitespace-nowrap rounded-lg bg-gradient-to-r from-[#453D89] to-[#C8499A] px-4 text-xs font-bold text-white disabled:opacity-50"
          :disabled="dateLoading || loading" @click="applyDateFilter">
          {{ t(dateLoading ? "Applying..." : "Apply") }}
        </button>

        <!-- Reset -->
        <button
          class="h-9 whitespace-nowrap rounded-lg border border-purple-100 px-3 text-xs font-bold text-[#453D89] hover:bg-purple-50 disabled:opacity-50"
          :disabled="dateLoading || loading" @click="resetDate">
          {{ t("Reset") }}
        </button>

      </div>

      <!-- Compact error message -->
      <p v-if="filterError" class="mt-2 text-xs font-semibold text-red-600">
        {{ filterError }}
      </p>

      <p class="mt-2 text-[10px] text-gray-600">
        {{ t("Showing records from") }}
        <strong>{{ formatDate(startDate) }}</strong> {{ t("to") }}
        <strong>{{ formatDate(endDate) }}</strong>.
      </p>
    </section>


    <!-- SHARED CHECK IN / OUT AND SHIFT -->
    <section v-if="hasEmployeeRecord" class="mt-4 grid grid-cols-1 items-stretch gap-3 lg:grid-cols-2">
      <article
        class="relative flex min-w-0 flex-col justify-center overflow-hidden rounded-2xl bg-gradient-to-br from-[#453D89] to-[#C8499A] p-5 text-white shadow-md">
        <div class="pointer-events-none absolute -right-8 -top-8 h-28 w-28 rounded-full bg-white/10"></div>

        <transition name="attendance-message">
          <div v-if="attendanceMessage" class="relative mb-3 rounded-lg border p-3 text-xs font-semibold"
            :class="attendanceMessageType === 'success' ? 'border-emerald-200/40 bg-emerald-400/20 text-white' : 'border-red-200/40 bg-red-400/20 text-white'"
            role="status" aria-live="polite">
            {{ attendanceMessageType === "success" ? "✓" : "!" }} {{ attendanceMessage }}
          </div>
        </transition>

        <div class="relative">
          <p class="text-xs font-semibold text-white/75">{{ t(isCheckedIn ? "Checked in" : "Attendance") }}</p>
          <h2 class="mt-2 text-3xl font-black tracking-tight">
            {{ lastCheckin ? formatTime(lastCheckin.time) : "--:--" }}
          </h2>
          <p class="mt-1 text-xs text-white/80">
            {{ t(isCheckedIn ? "Your attendance session is active." : "Record attendance using GPS.") }}
          </p>
          <p class="mt-1 text-[10px] text-white/70">{{ t("Filter") }}: {{ formatDate(startDate) }} – {{ formatDate(endDate) }}</p>
        </div>

        <div class="relative mt-5">
          <button type="button"
            class="flex min-h-11 w-full items-center justify-center gap-2 rounded-xl bg-white px-4 py-3 text-sm font-black text-[#453D89] shadow disabled:cursor-not-allowed disabled:opacity-60"
            :disabled="checkinLoading || locationLoading || loading || !employee.name || !rangeIncludesToday"
            @click="recordCheckin">
            <span v-if="checkinLoading || locationLoading"
              class="h-4 w-4 animate-spin rounded-full border-2 border-purple-200 border-t-[#453D89]"></span>
            {{ t(locationLoading ? "Getting GPS location..." : checkinLoading ? "Saving attendance..." : isCheckedIn ?
              "Check Out" : "Check In") }}
            <span v-if="!locationLoading && !checkinLoading">↗</span>
          </button>
          <p class="mt-2 text-center text-[10px] text-white/75">
            ⌖ {{ t("GPS is required. Actual current time is recorded.") }}
          </p>
          <p v-if="!rangeIncludesToday" class="mt-1 text-center text-[10px] text-white/80">
            {{ t("Include today in the date range to record attendance.") }}
          </p>
        </div>
      </article>

      <article class="flex min-w-0 flex-col rounded-2xl border border-[#eeeaf5] bg-white p-5 shadow-sm">
        <div class="flex items-center justify-between gap-3">
          <div class="flex items-center gap-3">
            <span
              class="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-purple-50 text-lg text-[#453D89]">◷</span>
            <div>
              <h3 class="text-sm font-extrabold">{{ t("My Shift") }}</h3>
              <p class="mt-1 text-[10px] text-gray-600">{{ t("Assignment overlapping the selected date range") }}</p>
            </div>
          </div>
          <button class="shrink-0 text-xs font-bold text-[#C8499A]" @click="openRoute('/app/shift-assignment')">{{ t("View") }}
            ↗</button>
        </div>

        <div v-if="currentShift" class="mt-4 flex flex-1 flex-col justify-center rounded-xl bg-[#faf8fd] p-4">
          <h4 class="break-words text-xl font-black text-[#453D89]">{{ currentShift.shift_type || t("Assigned Shift") }}
          </h4>
          <p class="mt-2 text-sm font-bold text-gray-700">
            {{ formatTime(currentShift.start_time) }} – {{ formatTime(currentShift.end_time) }}
          </p>
          <p class="mt-2 text-[10px] text-gray-600">
            {{ currentShift.start_date || "—" }} {{ t("to") }} {{ currentShift.end_date || "—" }}
          </p>
        </div>
        <div v-else class="mt-4 flex flex-1 items-center rounded-xl bg-[#faf8fd] p-4 text-xs text-gray-600">
          {{ t("No shift assignment found for the selected range.") }}
        </div>

        <button class="mt-3 w-full rounded-lg border border-purple-100 px-3 py-2.5 text-xs font-bold text-[#453D89]"
          @click="openRoute('/app/shift-assignment')">{{ t("View Shift Assignments") }} ↗</button>
      </article>

    </section>

    <!-- EMPLOYEE DASHBOARD -->
    <template v-if="isEmployee">
      <section class="mt-4 grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-3">

        <!-- ATTENDANCE -->
        <article class="rounded-xl border border-[#eeeaf5] bg-white p-4 shadow-sm">
          <CardHeading icon="◷" :title="t('Attendance Summary')" :link-label="t('View') + ' ↗'" @open="openRoute('/app/attendance')" />
          <p class="mt-3 text-[10px] text-gray-600">{{ formatDate(startDate) }} – {{ formatDate(endDate) }}</p>
          <div class="mt-3 grid grid-cols-3 gap-2">
            <div class="rounded-lg bg-emerald-50 p-3 text-center">
              <strong class="block text-xl font-black text-emerald-700">{{ attendanceSummary.present }}</strong>
              <span class="text-[10px] font-bold text-emerald-700">{{ t("Present") }}</span>
            </div>
            <div class="rounded-lg bg-red-50 p-3 text-center">
              <strong class="block text-xl font-black text-red-600">{{ attendanceSummary.absent }}</strong>
              <span class="text-[10px] font-bold text-red-600">{{ t("Absent") }}</span>
            </div>
            <div class="rounded-lg bg-purple-50 p-3 text-center">
              <strong class="block text-xl font-black text-[#453D89]">{{ attendanceSummary.half_day }}</strong>
              <span class="text-[10px] font-bold text-[#453D89]">{{ t("Half day") }}</span>
            </div>
          </div>
          <p class="mt-3 text-[10px] text-gray-600">{{ attendanceSummary.total }} {{ t("attendance record(s)") }}</p>
        </article>

        <!-- CHECK-IN HISTORY -->
        <article class="rounded-xl border border-[#eeeaf5] bg-white p-4 shadow-sm">
          <CardHeading icon="⌚" :title="t('Check-in History')" :link-label="t('View') + ' ↗'"
            @open="openRoute('/app/employee-checkin')" />
          <div v-if="dateCheckins.length" class="mt-3 divide-y divide-purple-50">
            <div v-for="checkin in dateCheckins.slice(0, 5)" :key="checkin.name"
              class="flex items-center justify-between gap-2 py-2">
              <span class="flex items-center gap-2">
                <span class="h-2 w-2 rounded-full"
                  :class="checkin.log_type === 'IN' ? 'bg-emerald-500' : 'bg-[#C8499A]'"></span>
                <strong class="text-xs">{{ t(checkin.log_type === "IN" ? "Check In" : "Check Out") }}</strong>
              </span>
              <span class="text-xs font-bold text-[#453D89]">{{ formatDateTime(checkin.time) }}</span>
            </div>
          </div>
          <p v-else class="mt-3 text-xs text-gray-600">{{ t("No check-in records in this date range.") }}</p>
          <p v-if="dateCheckins.length > 5" class="mt-2 text-[10px] text-gray-600">{{ t("Showing the first 5 records.") }}</p>
        </article>

        <!-- TASKS -->
        <article class="rounded-xl border border-[#eeeaf5] bg-white p-4 shadow-sm">
          <CardHeading icon="☑" :title="t('Assigned Tasks')" :link-label="t('View') + ' ↗'" @open="openRoute('/app/todo')" />
          <div v-if="employeeTasks.length" class="mt-3 divide-y divide-purple-50">
            <div v-for="task in employeeTasks.slice(0, 4)" :key="task.name" class="flex items-center gap-2 py-2">
              <span class="h-2 w-2 shrink-0 rounded-full bg-[#C8499A]"></span>
              <span class="min-w-0 flex-1 truncate text-xs text-gray-600">{{ task.description || task.name }}</span>
              <span class="text-[10px] text-gray-600">{{ t(task.status || "Open") }}</span>
            </div>
          </div>
          <p v-else class="mt-3 text-xs text-gray-600">{{ t("No tasks found.") }}</p>
        </article>

        <!-- LEAVE APPLICATIONS AND ALLOCATIONS -->
        <article class="rounded-xl border border-[#eeeaf5] bg-white p-4 shadow-sm">
          <CardHeading icon="▤" :title="t('Leave Overview')" :link-label="t('View') + ' ↗'"
            @open="openRoute('/app/leave-application')" />
          <p class="mt-3 text-[10px] font-bold text-gray-600">{{ t("Leave applications in selected range") }}</p>
          <div v-if="leaveApplications.length" class="mt-2 divide-y divide-purple-50">
            <div v-for="leave in leaveApplications.slice(0, 4)" :key="leave.name" class="py-2">
              <div class="flex items-center justify-between gap-2">
                <strong class="text-xs text-gray-700">{{ leave.leave_type || t("Leave") }}</strong>
                <span class="rounded-full bg-purple-50 px-2 py-1 text-[9px] font-bold text-[#453D89]">{{ leave.status ||
                  t("Pending") }}</span>
              </div>
              <p class="mt-1 text-[10px] text-gray-600">{{ leave.from_date }} – {{ leave.to_date }}</p>
            </div>
          </div>
          <p v-else class="mt-2 text-xs text-gray-600">{{ t("No leave applications in this range.") }}</p>

          <div class="mt-3 border-t border-purple-50 pt-3">
            <p class="text-[10px] font-bold text-gray-600">{{ t("Active leave allocations") }}</p>
            <div v-if="leaveBalances.length" class="mt-2 grid grid-cols-2 gap-2">
              <div v-for="leave in leaveBalances.slice(0, 4)" :key="leave.name" class="rounded-lg bg-[#faf8fd] p-3">
                <strong class="block text-lg font-black text-[#453D89]">{{ Number(leave.allocated ||
                  0).toLocaleString(currentDateLocale()) }}</strong>
                <span class="mt-1 block text-xs text-gray-600">{{ leave.leave_type }}</span>
              </div>
            </div>
            <p v-else class="mt-2 text-xs text-gray-600">{{ t("No allocation overlaps this range.") }}</p>
          </div>
        </article>

        <!-- SALARY SLIPS -->

        <article class="rounded-xl border border-[#eeeaf5] bg-white p-4 shadow-sm">
          <CardHeading icon="₹" :title="t('Salary Slips')" :link-label="t('View') + ' ↗'" @open="openRoute('/app/salary-slip')" />

          <div v-if="salarySlips.length" class="mt-3 divide-y divide-purple-50">
            <div v-for="slip in salarySlips.slice(0, 5)" :key="slip.name"
              class="flex items-center justify-between gap-3 py-3">
              <div class="min-w-0 flex-1">
                <strong class="block break-all text-sm font-black text-[#453D89]">
                  ₹{{ salaryVisible ? Number(slip.net_pay || 0).toLocaleString(currentDateLocale()) : "••••••" }}
                </strong>

                <p class="mt-1 text-[10px] text-gray-500">
                  {{ slip.start_date || "—" }} – {{ slip.end_date || "—" }}
                </p>

                <p class="mt-1 truncate text-[9px] text-gray-600">
                  {{ slip.name }}
                </p>
              </div>

              <div class="flex shrink-0 items-center gap-2">
                <button class="rounded-md px-2 py-1 text-[10px] font-bold text-[#C8499A] hover:bg-pink-50"
                  @click="salaryVisible = !salaryVisible">
                  {{ t(salaryVisible ? "Hide" : "Show") }}
                </button>

                <button
                  class="flex items-center gap-1 rounded-lg bg-gradient-to-r from-[#453D89] to-[#C8499A] px-3 py-2 text-[10px] font-bold text-white"
                  @click="downloadSalarySlip(slip.name)">
                  <span>↓</span>
                  PDF
                </button>
              </div>
            </div>
          </div>

          <p v-else class="mt-3 text-xs text-gray-600">
            {{ t("No salary slips available.") }}
          </p>
        </article>

        <!-- HOLIDAYS -->
        <article class="rounded-xl border border-[#eeeaf5] bg-white p-4 shadow-sm">
          <CardHeading icon="♧" :title="t('Holidays')" :link-label="t('View') + ' ↗'" @open="openRoute('/app/holiday-list')" />
          <p class="mt-3 text-[10px] text-gray-600">{{ t("Next 5 upcoming holidays") }}</p>
          <div v-if="holidays.length" class="mt-2 divide-y divide-purple-50">
            <div v-for="holiday in holidays" :key="holiday.holiday_date + holiday.description"
              class="flex items-center gap-3 py-2">
              <div
                class="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-purple-50 text-xs font-black text-[#453D89]">
                {{ datePart(holiday.holiday_date, "day") }}
                {{ datePart(holiday.holiday_date, "month") }}
              </div>
              <div class="min-w-0">
                <strong class="block text-xs text-gray-700">{{ holiday.description || t("Holiday") }}</strong>
                <span class="text-[10px] text-gray-600">{{ formatDate(holiday.holiday_date) }}</span>
              </div>
            </div>
          </div>
          <p v-else class="mt-3 text-xs text-gray-600">{{ t("No upcoming holidays.") }}</p>
        </article>
      </section>
    </template>

    <!-- ADMIN / HR DASHBOARD -->
    <template v-else>
      <section class="mt-4 grid grid-cols-2 gap-3 lg:grid-cols-4">
        <button class="rounded-xl border border-[#eeeaf5] bg-white p-4 text-left shadow-sm"
          @click="openRoute('/app/employee')">
          <span class="grid h-9 w-9 place-items-center rounded-lg bg-purple-50 text-lg text-[#453D89]">♙</span>
          <strong class="mt-3 block text-sm font-extrabold">{{ t("Employees") }}</strong>
          <small class="mt-1 block text-xs text-gray-600">{{ metrics.employees }} {{ t("records") }}</small>
        </button>
        <button class="rounded-xl border border-[#eeeaf5] bg-white p-4 text-left shadow-sm"
          @click="openRoute('/app/leave-application')">
          <span class="grid h-9 w-9 place-items-center rounded-lg bg-pink-50 text-lg text-[#C8499A]">◷</span>
          <strong class="mt-3 block text-sm font-extrabold">{{ t("Leave Requests") }}</strong>
          <small class="mt-1 block text-xs text-gray-600">{{ metrics.pendingLeaves }} {{ t("in range") }}</small>
        </button>
        <button class="rounded-xl border border-[#eeeaf5] bg-white p-4 text-left shadow-sm"
          @click="openRoute('/app/attendance')">
          <span class="grid h-9 w-9 place-items-center rounded-lg bg-emerald-50 text-lg text-emerald-700">✓</span>
          <strong class="mt-3 block text-sm font-extrabold">{{ t("Attendance") }}</strong>
          <small class="mt-1 block text-xs text-gray-600">{{ metrics.attendanceRecords }} {{ t("records") }}</small>
        </button>
        <button class="rounded-xl border border-[#eeeaf5] bg-white p-4 text-left shadow-sm"
          @click="openRoute('/app/salary-slip')">
          <span class="grid h-9 w-9 place-items-center rounded-lg bg-orange-50 text-lg text-orange-600">₹</span>
          <strong class="mt-3 block text-sm font-extrabold">{{ t("Payroll") }}</strong>
          <small class="mt-1 block text-xs text-gray-600">{{ metrics.salarySlips }} {{ t("slips in range") }}</small>
        </button>
      </section>

      <section class="mt-5">
        <div class="mb-3 flex flex-wrap items-center justify-between gap-3">
          <div>
            <p class="text-[9px] font-extrabold tracking-widest text-[#C8499A]">{{ t(isHR ? "HR OPERATIONS" :
              "ADMINOVERVIEW") }}</p>
            <h2 class="mt-1 text-xl font-black">{{ t("Workforce Overview") }}</h2>
            <p class="mt-1 text-[10px] text-gray-600">{{ formatDate(startDate) }} – {{ formatDate(endDate) }}</p>
          </div>
          <button class="rounded-lg border border-purple-100 bg-white px-3 py-2 text-xs font-bold text-[#453D89]"
            :disabled="loading || dateLoading" @click="loadDashboard">↻ {{ t("Refresh") }}</button>
        </div>

        <div class="grid grid-cols-2 gap-3 lg:grid-cols-3 xl:grid-cols-6">
          <button v-for="metric in metricCards" :key="metric.label"
            class="min-w-0 rounded-xl border border-[#eeeaf5] bg-white p-4 text-left shadow-sm"
            @click="openRoute(metric.route)">
            <span class="grid h-9 w-9 place-items-center rounded-lg text-lg" :class="metric.color">{{ metric.icon
            }}</span>
            <span class="mt-3 block text-[10px] font-semibold text-gray-600">{{ metric.label }}</span>
            <strong class="mt-1 block break-words text-xl font-black">{{ metric.value }}</strong>
            <small class="mt-1 block text-[10px] text-[#453D89]">{{ metric.note }}</small>
          </button>
        </div>
      </section>

      <section class="mt-4 grid grid-cols-1 gap-3 xl:grid-cols-2">
        <!-- ATTENDANCE OVERVIEW -->
        <article class="rounded-xl border border-[#eeeaf5] bg-white p-4 shadow-sm">
          <div class="flex items-center justify-between gap-2">
            <div>
              <h2 class="text-base font-black">{{ t("Attendance Overview") }}</h2>
              <p class="mt-1 text-[10px] text-gray-600">{{ formatDate(startDate) }} – {{ formatDate(endDate) }}</p>
            </div>
            <button class="text-xs font-bold text-[#C8499A]" @click="openRoute('/app/attendance')">{{ t("View all") }} ↗</button>
          </div>
          <div class="mt-4 space-y-3">
            <div class="flex items-center justify-between text-xs"><span>{{ t("Present") }}</span><strong>{{ metrics.present
            }}</strong></div>
            <div class="flex items-center justify-between text-xs"><span>{{ t("Absent") }}</span><strong>{{ metrics.absent
            }}</strong></div>
            <div class="flex items-center justify-between text-xs"><span>{{ t("Other attendance records") }}</span><strong>{{
              Math.max(0, metrics.attendanceRecords - metrics.present - metrics.absent) }}</strong></div>
          </div>
          <div class="mt-4 h-2 overflow-hidden rounded-full bg-purple-50">
            <div class="h-full rounded-full bg-gradient-to-r from-[#453D89] to-[#C8499A]"
              :style="{ width: attendancePercent + '%' }"></div>
          </div>
          <p class="mt-2 text-[10px] text-gray-600">{{ attendancePercent }}% {{ t("present against total employee count for this range.") }}</p>
        </article>

        <!-- HR ONLY: EMPLOYEE CHECK-IN / CHECK-OUT TABLE -->
        <section v-if="isHR" class="mt-4 overflow-hidden rounded-2xl border border-purple-100 bg-white shadow-sm">

          <div class="border-b border-purple-50 p-4">
            <h2 class="text-base font-black text-[#453D89]">
              {{ t("Employee Check-in / Check-out") }}
            </h2>
            <p class="mt-1 text-xs text-gray-600">
              {{ formatDate(startDate) }} – {{ formatDate(endDate) }}
            </p>
          </div>

          <div class="max-h-[320px] overflow-auto">
            <table class="w-full min-w-[440px] text-left">
              <thead class="sticky top-0 z-10 bg-gradient-to-r from-[#453D89] to-[#C8499A] text-white">
                <tr>
                  <th class="px-4 py-3 text-xs">{{ t("Employee Name") }}</th>
                  <th class="px-4 py-3 text-xs">{{ t("Check In") }}</th>
                  <th class="px-4 py-3 text-xs">{{ t("Check Out") }}</th>
                </tr>
              </thead>

              <tbody class="divide-y divide-purple-50">
                <tr v-for="row in adminEmployeeCheckins" :key="row.employee + '-' + row.date"
                  class="hover:bg-purple-50/50">

                  <td class="px-4 py-3 text-sm font-semibold">
                    {{ row.employee_name }}
                  </td>

                  <td class="px-4 py-3 text-xs font-bold text-emerald-700">
                    {{ row.check_in ? formatTime(row.check_in) : '—' }}
                  </td>

                  <td class="px-4 py-3 text-xs font-bold text-[#C8499A]">
                    {{ row.check_out ? formatTime(row.check_out) : '—' }}
                  </td>
                </tr>

                <tr v-if="employeeCheckinError">
                  <td colspan="3" class="px-4 py-8 text-center text-xs text-red-600">
                    {{ employeeCheckinError }}
                  </td>
                </tr>

                <tr v-else-if="!adminEmployeeCheckins.length">
                  <td colspan="3" class="px-4 py-8 text-center text-xs text-gray-600">
                    {{ t("No employee check-in records found for this date range.") }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </section>

        <!-- LEAVE APPLICATIONS -->
        <article class="rounded-xl border border-[#eeeaf5] bg-white p-4 shadow-sm">
          <div class="flex items-center justify-between gap-2">
            <div>
              <h2 class="text-base font-black">{{ t("Leave Applications") }}</h2>
              <p class="mt-1 text-[10px] text-gray-600">{{ t("Applications overlapping the selected range") }}</p>
            </div>
            <button class="text-xs font-bold text-[#C8499A]" @click="openRoute('/app/leave-application')">{{ t("View all") }}
              ↗</button>
          </div>
          <div v-if="adminLeaveApplications.length" class="mt-3 divide-y divide-purple-50">
            <div v-for="leave in adminLeaveApplications.slice(0, 6)" :key="leave.name"
              class="flex items-center justify-between gap-3 py-2">
              <div class="min-w-0">
                <strong class="block truncate text-xs">{{ leave.employee_name || leave.employee || t("Employee")
                }}</strong>
                <p class="mt-1 text-[10px] text-gray-600">{{ leave.leave_type }} · {{ leave.from_date }} – {{
                  leave.to_date }}</p>
              </div>
              <span class="shrink-0 rounded-full bg-purple-50 px-2 py-1 text-[9px] font-bold text-[#453D89]">{{
                t(leave.status || "Pending") }}</span>
            </div>
          </div>
          <p v-else class="mt-3 text-xs text-gray-600">{{ t("No leave applications overlap this range.") }}</p>
        </article>

        <!-- PAYROLL SUMMARY -->
        <article class="rounded-xl border border-[#eeeaf5] bg-white p-4 shadow-sm">
          <div class="flex items-center justify-between gap-2">
            <div>
              <h2 class="text-base font-black">{{ t("Payroll Summary") }}</h2>
              <p class="mt-1 text-[10px] text-gray-600">{{ t("Submitted salary slips overlapping the selected range") }}</p>
            </div>
            <button class="text-xs font-bold text-[#C8499A]" @click="openRoute('/app/salary-slip')">{{ t("View all") }} ↗</button>
          </div>
          <strong class="mt-4 block text-2xl font-black text-[#453D89]">₹{{ Number(metrics.payroll ||
            0).toLocaleString(currentDateLocale()) }}</strong>
          <p class="mt-1 text-xs text-gray-600">{{ metrics.salarySlips }} {{ t("salary slips") }}</p>
          <div v-if="adminSalarySlips.length" class="mt-3 divide-y divide-purple-50">
            <div v-for="slip in adminSalarySlips.slice(0, 5)" :key="slip.name"
              class="flex items-center justify-between gap-2 py-2">
              <div class="min-w-0">
                <strong class="block truncate text-xs">{{ slip.employee_name || slip.employee || slip.name }}</strong>
                <p class="mt-1 text-[10px] text-gray-600">{{ slip.start_date }} – {{ slip.end_date }}</p>
              </div>
              <strong class="text-xs text-[#453D89]">₹{{ Number(slip.net_pay || 0).toLocaleString(currentDateLocale()) }}</strong>
            </div>
          </div>
          <p v-else class="mt-3 text-xs text-gray-600">{{ t("No salary slips overlap this range.") }}</p>
        </article>

        <!-- HOLIDAYS -->
        <article class="rounded-xl border border-[#eeeaf5] bg-white p-4 shadow-sm">
          <div class="flex items-center justify-between gap-2">
            <div>
              <h2 class="text-base font-black">{{ t("Holidays") }}</h2>
              <p class="mt-1 text-[10px] text-gray-600">{{ t("Next 5 upcoming holidays") }}</p>
            </div>
            <button class="text-xs font-bold text-[#C8499A]" @click="openRoute('/app/holiday-list')">{{ t("View all") }} ↗</button>
          </div>
          <div v-if="holidays.length" class="mt-3 divide-y divide-purple-50">
            <div v-for="holiday in holidays" :key="holiday.holiday_date + holiday.description"
              class="flex items-center gap-3 py-2">
              <div
                class="grid h-10 w-10 shrink-0 place-items-center rounded-lg bg-purple-50 text-xs font-black text-[#453D89]">
                {{ datePart(holiday.holiday_date, "day") }} {{ datePart(holiday.holiday_date, "month") }}
              </div>
              <div>
                <strong class="block text-xs text-gray-700">{{ holiday.description || t("Holiday") }}</strong>
                <span class="text-[10px] text-gray-600">{{ formatDate(holiday.holiday_date) }}</span>
              </div>
            </div>
          </div>
          <p v-else class="mt-3 text-xs text-gray-600">{{ t("No upcoming holidays found for the available holiday lists.") }}
          </p>
        </article>


        <article class="rounded-xl border border-[#eeeaf5] bg-white p-4 shadow-sm xl:col-span-2">
          <!-- Header -->
          <div class="flex items-center justify-between gap-2">
            <div>
              <h2 class="text-base font-black text-[#25213a]">{{ t("Quick Links") }}</h2>
              <p class="mt-1 text-[10px] text-gray-600">
                {{ t("Access your HRMS tools quickly") }}
              </p>
            </div>
            <span class="rounded-full bg-purple-50 px-3 py-1 text-[10px] font-bold text-[#453D89]">
              {{ t("Shortcuts") }}
            </span>
          </div>

          <!-- Quick Link Grid -->
          <div class="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">

            <!-- Employees -->
            <button @click="openRoute('/app/employee')"
              class="group flex items-center gap-3 rounded-xl border border-purple-100 bg-[#faf9fd] p-3 text-left transition hover:border-[#453D89] hover:bg-purple-50">
              <span
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-r from-[#453D89] to-[#C8499A] text-lg text-white">
                <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <path d="M16 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2" />
                  <circle cx="10" cy="7" r="4" />
                  <path d="M20 21v-2a4 4 0 0 0-3-3.87M16 3.13a4 4 0 0 1 0 7.75" />
                </svg>
              </span>
              <span class="min-w-0">
                <strong class="block text-xs font-bold text-[#453D89]">{{ t("Employees") }}</strong>
                <span class="mt-1 block text-[10px] text-gray-600">{{ t("Employee directory") }}</span>
              </span>
            </button>

            <!-- Attendance -->
            <button @click="openRoute('/app/attendance')"
              class="group flex items-center gap-3 rounded-xl border border-purple-100 bg-[#faf9fd] p-3 text-left transition hover:border-[#453D89] hover:bg-purple-50">
              <span
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-r from-[#453D89] to-[#C8499A] text-white">
                <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="4" width="18" height="17" rx="2" />
                  <path d="M16 2v4M8 2v4M3 10h18l-7 5-3-2-4 4" />
                </svg>
              </span>
              <span class="min-w-0">
                <strong class="block text-xs font-bold text-[#453D89]">{{ t("Attendance") }}</strong>
                <span class="mt-1 block text-[10px] text-gray-600">{{ t("Daily attendance") }}</span>
              </span>
            </button>

            <!-- Leave Applications -->
            <button @click="openRoute('/app/leave-application')"
              class="group flex items-center gap-3 rounded-xl border border-purple-100 bg-[#faf9fd] p-3 text-left transition hover:border-[#453D89] hover:bg-purple-50">
              <span
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-r from-[#453D89] to-[#C8499A] text-white">
                <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="4" y="5" width="16" height="16" rx="2" />
                  <path d="M8 3v4M16 3v4M4 10h16M9 15l2 2 4-4" />
                </svg>
              </span>
              <span class="min-w-0">
                <strong class="block text-xs font-bold text-[#453D89]">{{ t("Leave Requests") }}</strong>
                <span class="mt-1 block text-[10px] text-gray-600">{{ t("Manage leave") }}</span>
              </span>
            </button>

            <!-- Salary Slips -->
            <button @click="openRoute('/app/salary-slip')"
              class="group flex items-center gap-3 rounded-xl border border-purple-100 bg-[#faf9fd] p-3 text-left transition hover:border-[#453D89] hover:bg-purple-50">
              <span
                class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-gradient-to-r from-[#453D89] to-[#C8499A] text-white">
                <svg xmlns="http://www.w3.org/2000/svg" width="21" height="21" viewBox="0 0 24 24" fill="none"
                  stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">
                  <rect x="3" y="5" width="18" height="14" rx="2" />
                  <path d="M3 10h18M7 15h3" />
                  <path d="M16 14v3m-1.5-1.5h3" />
                </svg>
              </span>
              <span class="min-w-0">
                <strong class="block text-xs font-bold text-[#453D89]">{{ t("Salary Slips") }}</strong>
                <span class="mt-1 block text-[10px] text-gray-600">{{ t("Payroll records") }}</span>
              </span>
            </button>

          </div>
        </article>

      </section>
    </template>
  </main>
</template>

<script setup>
import {
  ref,
  computed,
  nextTick,
  onMounted,
  onBeforeUnmount,
  defineComponent,
  h,
} from "vue";

function t(text) {
  return window.frappe?._ ? window.frappe._(text) : text;
}

function currentDateLocale() {
  return window.frappe?.boot?.lang || navigator.language;
}

/* -------------------------------------------------------
   REUSABLE CARD HEADING
------------------------------------------------------- */
const CardHeading = defineComponent({
  props: {
    icon: { type: String, default: "•" },
    title: { type: String, required: true },
    linkLabel: { type: String, default: "" },
  },
  emits: ["open"],
  setup(props, { emit }) {
    return () =>
      h("div", { class: "flex items-center justify-between gap-3" }, [
        h("div", { class: "flex min-w-0 items-center gap-3" }, [
          h("span", {
            class: "grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-purple-50 text-base font-bold text-[#453D89]",
          }, props.icon),
          h("h3", { class: "text-sm font-extrabold" }, props.title),
        ]),
        props.linkLabel
          ? h("button", {
            class: "shrink-0 text-[10px] font-bold text-[#C8499A] hover:underline",
            onClick: () => emit("open"),
          }, props.linkLabel)
          : null,
      ]);
  },
});

/* -------------------------------------------------------
   STATE
------------------------------------------------------- */
const loading = ref(false);
const dateLoading = ref(false);
const checkinLoading = ref(false);
const locationLoading = ref(false);
const errorMessage = ref("");
const filterError = ref("");
const filterApplied = ref(false);

const attendanceMessage = ref("");
const attendanceMessageType = ref("success");
let attendanceMessageTimer = null;

const loggedUser = ref("");
const userFullName = ref("");
const userRoles = ref([]);
const userImage = ref("");
const employee = ref({});

const isEmployee = ref(false);
const isHR = ref(false);
const hasAdminRole = ref(false);

const todayISO = localDate();
const startDate = ref(todayISO);
const endDate = ref(todayISO);

const notifications = ref([]);
const unreadCount = ref(0);
const notificationsOpen = ref(false);
const notificationsLoading = ref(false);
const workspaceMenuOpen = ref(false);
const workspaceMenuItems = ref([]);
const profileMenuOpen = ref(false);
const selectedLanguage = ref(window.frappe?.boot?.lang || "en");
const languageSaving = ref(false);
const languageError = ref("");
const languagePicker = ref(null);
const languagePickerButton = ref(null);
const languageSearchInput = ref(null);
const languagePickerOpen = ref(false);
const languageSearch = ref("");
const availableLanguages = computed(() => {
  const languages = Object.entries(window.frappe?.boot?.lang_dict || {})
    .map(([label, value]) => ({ label, value }))
    .sort((a, b) => a.label.localeCompare(b.label));

  if (!languages.some((language) => language.value === selectedLanguage.value)) {
    languages.push({ label: selectedLanguage.value, value: selectedLanguage.value });
  }

  return languages;
});
const selectedLanguageLabel = computed(() =>
  availableLanguages.value.find((language) => language.value === selectedLanguage.value)?.label || selectedLanguage.value
);
const filteredLanguages = computed(() => {
  const query = languageSearch.value.trim().toLocaleLowerCase();
  if (!query) return availableLanguages.value;

  return availableLanguages.value.filter(({ label, value }) =>
    `${label} ${value}`.toLocaleLowerCase().includes(query)
  );
});

const attendanceSummary = ref({
  present: 0,
  absent: 0,
  half_day: 0,
  total: 0,
});

const metrics = ref({
  employees: 0,
  departments: 0,
  present: 0,
  absent: 0,
  pendingLeaves: 0,
  attendanceRecords: 0,
  payroll: 0,
  salarySlips: 0,
});

const employeeTasks = ref([]);
const leaveBalances = ref([]);
const leaveApplications = ref([]);
const adminLeaveApplications = ref([]);
const holidays = ref([]);
const salarySlips = ref([]);
const adminSalarySlips = ref([]);
const currentShift = ref(null);
const lastCheckin = ref(null);
const dateCheckins = ref([]);
const adminEmployeeCheckins = ref([]);
const employeeCheckinError = ref("");
const salaryVisible = ref(false);

let notificationTimer = null;

/* -------------------------------------------------------
   COMPUTED VALUES
------------------------------------------------------- */
const hasEmployeeRecord = computed(() => Boolean(employee.value.name));

const rangeIncludesToday = computed(() =>
  startDate.value <= todayISO && endDate.value >= todayISO
);

const displayName = computed(() =>
  employee.value.employee_name ||
  (loggedUser.value && loggedUser.value !== "Guest"
    ? loggedUser.value.split("@")[0]
    : "there")
);

const profileDisplayName = computed(() =>
  userFullName.value || displayName.value
);

const initials = computed(() =>
  String(displayName.value || "U").trim().slice(0, 1).toUpperCase()
);

const profileInitials = computed(() =>
  String(profileDisplayName.value || "U").trim().slice(0, 1).toUpperCase()
);

const roleLabel = computed(() => {
  if (isEmployee.value) return t("EMPLOYEE WORKSPACE");
  if (isHR.value) return t("HUMAN RESOURCES WORKSPACE");
  return t("ADMINISTRATOR OVERVIEW");
});

const roleDisplay = computed(() => {
  if (isEmployee.value) return t("Employee");
  if (isHR.value) return t("HR Workspace");
  return t("Administrator");
});

const greeting = computed(() => {
  const hour = new Date().getHours();
  if (hour < 12) return t("morning");
  if (hour < 17) return t("afternoon");
  return t("evening");
});

const todayLabel = computed(() =>
  new Date().toLocaleDateString(currentDateLocale(), {
    weekday: "short",
    day: "numeric",
    month: "short",
    year: "numeric",
  })
);

const isCheckedIn = computed(() => lastCheckin.value?.log_type === "IN");

const attendancePercent = computed(() =>
  metrics.value.employees
    ? Math.min(100, Math.round((metrics.value.present / metrics.value.employees) * 100))
    : 0
);

const metricCards = computed(() => [
  {
    label: t("Total Employees"),
    value: metrics.value.employees,
    note: t("Employee records"),
    icon: "♙",
    color: "bg-purple-50 text-[#453D89]",
    route: "/app/employee",
  },
  {
    label: t("Departments"),
    value: metrics.value.departments,
    note: t("Organisation structure"),
    icon: "▦",
    color: "bg-pink-50 text-[#C8499A]",
    route: "/app/department",
  },
  {
    label: t("Present"),
    value: metrics.value.present,
    note: t("Selected date range"),
    icon: "✓",
    color: "bg-emerald-50 text-emerald-700",
    route: "/app/attendance",
  },
  {
    label: t("Absent"),
    value: metrics.value.absent,
    note: t("Selected date range"),
    icon: "×",
    color: "bg-red-50 text-red-600",
    route: "/app/attendance",
  },
  {
    label: t("Leave Applications"),
    value: metrics.value.pendingLeaves,
    note: t("Overlapping selected range"),
    icon: "◷",
    color: "bg-orange-50 text-orange-600",
    route: "/app/leave-application",
  },
  {
    label: t("Submitted Payroll"),
    value: "₹" + Number(metrics.value.payroll || 0).toLocaleString(currentDateLocale()),
    note: `${metrics.value.salarySlips} ${t("slips in range")}`,
    icon: "₹",
    color: "bg-purple-50 text-[#453D89]",
    route: "/app/salary-slip",
  },
]);

/* -------------------------------------------------------
   DATE / FORMAT HELPERS
------------------------------------------------------- */
function localDate(date = new Date()) {
  const pad = (value) => String(value).padStart(2, "0");
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())}`;
}

function formatDate(value) {
  if (!value) return "—";
  const date = new Date(`${value}T00:00:00`);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString(currentDateLocale(), {
    weekday: "short",
    day: "numeric",
    month: "short",
    year: "numeric",
  });
}

function formatDateTime(value) {
  if (!value) return "";
  const date = new Date(String(value).replace(" ", "T"));
  if (Number.isNaN(date.getTime())) return String(value);
  return date.toLocaleString(currentDateLocale(), {
    day: "numeric",
    month: "short",
    year: "numeric",
    hour: "2-digit",
    minute: "2-digit",
  });
}

function formatTime(value) {
  if (!value) return "—";
  const match = String(value).match(/(?:T|\s)?(\d{1,2}):(\d{2})/);
  if (!match) return String(value);
  let hours = Number(match[1]);
  const minutes = match[2];
  const suffix = hours >= 12 ? "PM" : "AM";
  hours = hours % 12 || 12;
  return `${String(hours).padStart(2, "0")}:${minutes} ${t(suffix)}`;
}

function datePart(value, part) {
  if (!value) return "—";
  const date = new Date(`${value}T00:00:00`);
  if (Number.isNaN(date.getTime())) return "—";
  return part === "day"
    ? date.getDate()
    : date.toLocaleDateString(currentDateLocale(), { month: "short" }).toUpperCase();
}

function openRoute(route) {
  if (route) window.location.href = route;
}

function loadWorkspaceMenu() {
  const links = document.querySelectorAll(
    ".body-sidebar-container .sidebar-items .standard-sidebar-item > a.item-anchor[href]"
  );

  workspaceMenuItems.value = Array.from(links)
    .map((link) => ({
      href: link.getAttribute("href"),
      label: link.querySelector(".sidebar-item-label")?.textContent?.trim(),
    }))
    .filter((item) => item.href && item.label);
}

function openWorkspaceRoute(route) {
  workspaceMenuOpen.value = false;
  openRoute(route);
}

function openGlobalSearch() {
  const searchButton = document.querySelector(
    "#navbar-modal-search, #desktop-navbar-modal-search"
  );

  if (!searchButton) {
    console.error("Frappe's global search control is not available.");
    return;
  }

  searchButton.click();
}

function openUserProfile() {
  profileMenuOpen.value = false;
  if (typeof window.frappe?.set_route !== "function") {
    console.error("Frappe routing is not available.");
    return;
  }

  window.frappe.set_route("Form", "User", loggedUser.value);
}

function toggleLanguagePicker() {
  if (languagePickerOpen.value) {
    closeLanguagePicker();
    return;
  }

  languagePickerOpen.value = true;
  nextTick(() => languageSearchInput.value?.focus());
}

function closeLanguagePicker(returnFocus = false) {
  languagePickerOpen.value = false;
  languageSearch.value = "";
  if (returnFocus) nextTick(() => languagePickerButton.value?.focus());
}

function handleLanguagePickerClickOutside(event) {
  const picker = languagePicker.value;
  if (languagePickerOpen.value && picker && !picker.contains(event.target)) {
    closeLanguagePicker();
  }
}

function selectLanguage(language) {
  closeLanguagePicker();
  changeLanguage(language);
}

async function changeLanguage(language) {
  const currentLanguage = window.frappe?.boot?.lang || "en";
  languageError.value = "";

  if (language === currentLanguage) return;

  selectedLanguage.value = language;
  languageSaving.value = true;

  try {
    await frappeRequest("/api/method/frappe.client.set_value", {
      method: "POST",
      body: JSON.stringify({
        doctype: "User",
        name: loggedUser.value,
        fieldname: "language",
        value: language,
      }),
    });
    window.location.reload();
  } catch (error) {
    console.error("Could not update dashboard language:", error);
    selectedLanguage.value = currentLanguage;
    languageError.value = t("Unable to update your language. Please try again.");
  } finally {
    languageSaving.value = false;
  }
}

function openHrSettings() {
  profileMenuOpen.value = false;
  if (typeof window.frappe?.set_route !== "function") {
    console.error("Frappe routing is not available.");
    return;
  }

  window.frappe.set_route("Form", "HR Settings", "HR Settings");
}

function signOut() {
  profileMenuOpen.value = false;
  if (typeof window.frappe?.app?.logout !== "function") {
    console.error("Frappe sign out is not available.");
    return;
  }

  window.frappe.app.logout();
}

function createEmployee() {
  if (typeof window.frappe?.new_doc !== "function") {
    console.error("Frappe's new document action is not available.");
    return;
  }

  window.frappe.new_doc("Employee");
}

function validateDateRange() {
  filterError.value = "";

  if (!startDate.value || !endDate.value) {
    filterError.value = t("Please select both a start date and an end date.");
    return false;
  }

  if (startDate.value > endDate.value) {
    filterError.value = t("Start date cannot be later than end date.");
    return false;
  }

  return true;
}

/* -------------------------------------------------------
   FRAPPE API HELPERS
------------------------------------------------------- */
function parseServerMessage(value) {
  try {
    const parsed = JSON.parse(value);
    return parsed.map((message) => {
      try {
        const item = JSON.parse(message);
        return item.message || message;
      } catch {
        return message;
      }
    }).join(" ");
  } catch {
    return value;
  }
}

async function frappeRequest(url, options = {}) {
  const headers = {
    Accept: "application/json",
    ...(options.headers || {}),
  };

  if (options.method && options.method !== "GET") {
    headers["Content-Type"] = "application/json";
    const csrf = window.frappe?.csrf_token;
    if (csrf) headers["X-Frappe-CSRF-Token"] = csrf;
  }

  const response = await fetch(url, {
    credentials: "same-origin",
    ...options,
    headers,
  });

  let payload = {};
  try {
    payload = await response.json();
  } catch {
    // Response did not contain JSON.
  }

  if (!response.ok || payload.exc) {
    const message = payload._server_messages
      ? parseServerMessage(payload._server_messages)
      : payload.exception || payload.message || `Request failed (${response.status})`;
    throw new Error(message);
  }

  return payload;
}

function queryString(params) {
  return new URLSearchParams(
    Object.entries(params).map(([key, value]) => [
      key,
      typeof value === "string" ? value : JSON.stringify(value),
    ])
  ).toString();
}

async function getList(
  doctype,
  {
    fields = ["name"],
    filters = [],
    orderBy = "modified desc",
    limit = 100,
  } = {}
) {
  const query = queryString({
    fields,
    filters,
    order_by: orderBy,
    limit_page_length: limit,
  });

  const response = await frappeRequest(
    `/api/resource/${encodeURIComponent(doctype)}?${query}`
  );
  return response.data || [];
}

async function getCount(doctype, filters = []) {
  const query = queryString({ doctype, filters });
  const response = await frappeRequest(
    `/api/method/frappe.client.get_count?${query}`
  );
  return Number(response.message || 0);
}

function rangeOverlapFilters(fromField, toField) {
  return [
    [fromField, "<=", endDate.value],
    [toField, ">=", startDate.value],
  ];
}

/* -------------------------------------------------------
   USER / ROLE DETECTION
------------------------------------------------------- */
async function getLoggedInUser() {
  const response = await frappeRequest("/api/method/frappe.auth.get_logged_user");
  loggedUser.value = response.message || "";

  if (!loggedUser.value || loggedUser.value === "Guest") {
    throw new Error(t("Please log in to view your HRMS dashboard."));
  }

  userFullName.value = "";
  userImage.value = "";
  employee.value = {};
  userRoles.value = [];

  try {
    const fields = encodeURIComponent(JSON.stringify(["name", "full_name", "user_image"]));
    const userResponse = await frappeRequest(
      `/api/resource/User/${encodeURIComponent(loggedUser.value)}?fields=${fields}`
    );
    userFullName.value = userResponse.data?.full_name || "";
    userImage.value = userResponse.data?.user_image || "";
  } catch (error) {
    console.warn("Could not load user profile:", error);
  }

  const bootRoles = window.frappe?.boot?.user?.roles;
  userRoles.value = Array.isArray(bootRoles) ? bootRoles : [];
  const roles = userRoles.value.map((role) => String(role).toLowerCase());

  hasAdminRole.value =
    loggedUser.value === "Administrator" || roles.includes("system manager");

  isHR.value =
    !hasAdminRole.value &&
    roles.some((role) => ["hr manager", "hr user", "employee manager"].includes(role));

  // Find a linked Employee record for any login, including HR/Admin accounts.
  try {
    const matches = await getList("Employee", {
      fields: [
        "name", "employee_name", "user_id", "department", "designation",
        "status", "date_of_joining", "company", "holiday_list",
      ],
      filters: [["user_id", "=", loggedUser.value]],
      limit: 1,
    });
    employee.value = matches[0] || {};
  } catch (error) {
    console.warn("Could not load linked Employee:", error);
  }

  isEmployee.value = Boolean(employee.value.name) && !hasAdminRole.value && !isHR.value;
}

/* -------------------------------------------------------
   NOTIFICATIONS
------------------------------------------------------- */
function isRead(notification) {
  return notification?.read === 1 || notification?.read === true || notification?.read === "1";
}

function notificationMessage(notification) {
  const content = notification.email_content || notification.message || "";
  if (!content) return t("You have a new notification.");
  const plain = String(content).replace(/<[^>]*>/g, " ").replace(/\s+/g, " ").trim();
  return plain.length > 120 ? plain.slice(0, 117) + "..." : plain;
}

async function loadNotifications() {
  if (!loggedUser.value || loggedUser.value === "Guest") return;

  notificationsLoading.value = true;
  try {
    notifications.value = await getList("Notification Log", {
      fields: [
        "name", "subject", "email_content", "creation", "read",
        "document_type", "document_name", "type",
      ],
      filters: [["for_user", "=", loggedUser.value]],
      orderBy: "creation desc",
      limit: 30,
    });

    unreadCount.value = notifications.value.filter((item) => !isRead(item)).length;
  } catch (error) {
    console.error("Could not load notifications. Check Notification Log permissions and fields:", error);
  } finally {
    notificationsLoading.value = false;
  }
}

async function toggleNotifications() {
  notificationsOpen.value = !notificationsOpen.value;
  if (notificationsOpen.value) await loadNotifications();
}

async function markNotificationRead(notification) {
  if (!notification?.name || isRead(notification)) return;

  try {
    await frappeRequest(
      `/api/resource/Notification%20Log/${encodeURIComponent(notification.name)}`,
      {
        method: "PUT",
        body: JSON.stringify({ read: 1 }),
      }
    );

    notification.read = 1;
    unreadCount.value = notifications.value.filter((item) => !isRead(item)).length;
  } catch (error) {
    console.error("Could not mark notification as read:", error);
  }
}

async function markAllNotificationsRead() {
  for (const notification of notifications.value.filter((item) => !isRead(item))) {
    await markNotificationRead(notification);
  }
}

async function openNotification(notification) {
  await markNotificationRead(notification);
  notificationsOpen.value = false;

  if (notification.document_type && notification.document_name) {
    const route = `/app/${notification.document_type.toLowerCase().replace(/\s+/g, "-")}/${encodeURIComponent(notification.document_name)}`;
    openRoute(route);
  }
}

/* -------------------------------------------------------
   EMPLOYEE DATA FOR SELECTED DATE RANGE
------------------------------------------------------- */
async function loadEmployeeDashboard() {
  if (!employee.value.name) return;

  const id = employee.value.name;
  const start = startDate.value;
  const end = endDate.value;

  const results = await Promise.allSettled([
    // Tasks with a due date in the selected range.
    getList("ToDo", {
      fields: ["name", "description", "status", "date"],
      filters: [
        ["allocated_to", "=", loggedUser.value],
        ["status", "!=", "Closed"],
        ["date", ">=", start],
        ["date", "<=", end],
      ],
      orderBy: "date asc",
      limit: 20,
    }),

    // Attendance in range.
    getList("Attendance", {
      fields: ["name", "attendance_date", "status"],
      filters: [
        ["employee", "=", id],
        ["attendance_date", ">=", start],
        ["attendance_date", "<=", end],
        ["docstatus", "=", 1],
      ],
      orderBy: "attendance_date desc",
      limit: 1000,
    }),

    // Submitted salary slips whose salary period overlaps the range.
    getList("Salary Slip", {
      fields: ["name", "employee", "net_pay", "start_date", "end_date", "docstatus"],
      filters: [
        ["employee", "=", id],
        ["docstatus", "=", 1],
        ["start_date", "<=", end],
        ["end_date", ">=", start],
      ],
      orderBy: "start_date desc",
      limit: 1000,
    }),

    // Check-in records within the selected range.
    getList("Employee Checkin", {
      fields: ["name", "time", "log_type", "latitude", "longitude"],
      filters: [
        ["employee", "=", id],
        ["time", ">=", `${start} 00:00:00`],
        ["time", "<=", `${end} 23:59:59`],
      ],
      orderBy: "time desc",
      limit: 1000,
    }),

    // Leave applications overlapping the selected range.
    getList("Leave Application", {
      fields: ["name", "employee", "leave_type", "from_date", "to_date", "status", "docstatus"],
      filters: [
        ["employee", "=", id],
        ...rangeOverlapFilters("from_date", "to_date"),
      ],
      orderBy: "from_date desc",
      limit: 1000,
    }),

    // Leave allocations overlapping the selected range.
    getList("Leave Allocation", {
      fields: [
        "name", "leave_type", "total_leaves_allocated",
        "new_leaves_allocated", "from_date", "to_date", "docstatus",
      ],
      filters: [
        ["employee", "=", id],
        ["docstatus", "=", 1],
        ...rangeOverlapFilters("from_date", "to_date"),
      ],
      orderBy: "leave_type asc",
      limit: 1000,
    }),
  ]);

  employeeTasks.value = results[0].status === "fulfilled" ? results[0].value : [];

  const attendance = results[1].status === "fulfilled" ? results[1].value : [];
  attendanceSummary.value = {
    present: attendance.filter((row) => row.status === "Present").length,
    absent: attendance.filter((row) => row.status === "Absent").length,
    half_day: attendance.filter((row) => row.status === "Half Day").length,
    total: attendance.length,
  };

  salarySlips.value = results[2].status === "fulfilled" ? results[2].value : [];
  dateCheckins.value = results[3].status === "fulfilled" ? results[3].value : [];
  leaveApplications.value = results[4].status === "fulfilled" ? results[4].value : [];

  const allocations = results[5].status === "fulfilled" ? results[5].value : [];
  leaveBalances.value = allocations.map((row) => ({
    ...row,
    allocated: row.new_leaves_allocated ?? row.total_leaves_allocated ?? 0,
    leave_type: row.leave_type || "Leave",
  }));

  // Only today's check-in state determines the live check-in/out button.
  lastCheckin.value = rangeIncludesToday.value
    ? dateCheckins.value
      .filter((row) => String(row.time || "").slice(0, 10) === todayISO)
      .sort((a, b) => String(a.time).localeCompare(String(b.time)))[
    dateCheckins.value.filter((row) => String(row.time || "").slice(0, 10) === todayISO).length - 1
    ] || null
    : null;

  await loadShiftForRange(id, start, end);
  await loadHolidays();
}

// salary slip download helper
const downloadSalarySlip = (slipName) => {
  if (!slipName) return;

  const url =
    `/api/method/frappe.utils.print_format.download_pdf` +
    `?doctype=Salary%20Slip` +
    `&name=${encodeURIComponent(slipName)}` +
    `&format=Standard` +
    `&no_letterhead=0`;

  window.open(url, "_blank");
};

/* -------------------------------------------------------
   SHIFT AND HOLIDAYS
------------------------------------------------------- */
async function loadShiftForRange(employeeId, start, end) {
  try {
    const assignments = await getList("Shift Assignment", {
      fields: ["name", "shift_type", "start_date", "end_date", "docstatus"],
      filters: [
        ["employee", "=", employeeId],
        ["docstatus", "=", 1],
        ["start_date", "<=", end],
        ["end_date", ">=", start],
      ],
      orderBy: "start_date desc",
      limit: 20,
    });

    currentShift.value = assignments[0] || null;

    if (currentShift.value?.shift_type) {
      const response = await frappeRequest(
        `/api/resource/Shift%20Type/${encodeURIComponent(currentShift.value.shift_type)}`
      );
      currentShift.value = { ...currentShift.value, ...response.data };
    }
  } catch (error) {
    console.warn("Could not load shift assignment:", error);
    currentShift.value = null;
  }
}

async function getHolidayListAssignments(filters = []) {
  try {
    return await getList("Holiday List Assignment", {
      fields: ["name", "holiday_list", "assigned_to", "from_date"],
      filters: [["docstatus", "=", 1], ...filters],
      orderBy: "from_date desc",
      limit: 1000,
    });
  } catch (error) {
    console.warn("Could not load Holiday List Assignments:", error);
    return [];
  }
}

function stripHtml(value) {
  if (!value) return "";
  const element = document.createElement("div");
  element.innerHTML = String(value);
  return (element.textContent || "").replace(/\s+/g, " ").trim();
}

async function fetchUpcomingHolidays(listNames) {
  const names = [...listNames];
  const unique = new Map();

  const responses = await Promise.allSettled(
    names.map((listName) =>
      frappeRequest(`/api/resource/Holiday%20List/${encodeURIComponent(listName)}`)
    )
  );

  responses.forEach((result, index) => {
    if (result.status === "rejected") {
      console.warn(`Could not load holidays from ${names[index]}:`, result.reason);
      return;
    }

    const rows = result.value.data?.holidays || [];
    rows
      .filter((holiday) => holiday.holiday_date && holiday.holiday_date >= todayISO)
      .forEach((holiday) => {
        const description = stripHtml(holiday.description);
        const key = `${holiday.holiday_date}|${description}`;
        if (!unique.has(key)) unique.set(key, { ...holiday, description });
      });
  });

  return [...unique.values()]
    .sort((a, b) => String(a.holiday_date).localeCompare(String(b.holiday_date)))
    .slice(0, 5);
}

async function getAllHolidayListNames() {
  try {
    const lists = await getList("Holiday List", {
      fields: ["name"],
      limit: 100,
    });
    return lists.map((list) => list.name);
  } catch (error) {
    console.warn("Could not retrieve holiday lists from the backend:", error);
    return [];
  }
}

async function loadHolidays() {
  const holidayListNames = new Set();

  // Holiday lists assigned via Holiday List Assignment.
  let assignments = [];
  if (isEmployee.value) {
    // Employees: prefer their own assignments, then fall back to the company's.
    if (employee.value.name) {
      assignments = await getHolidayListAssignments([
        ["assigned_to", "=", employee.value.name],
      ]);
    }
    if (!assignments.length && employee.value.company) {
      assignments = await getHolidayListAssignments([
        ["assigned_to", "=", employee.value.company],
      ]);
    }
  } else {
    // Admin/HR: use every submitted assignment.
    assignments = await getHolidayListAssignments();
  }

  assignments.forEach((row) => {
    if (row.holiday_list) holidayListNames.add(row.holiday_list);
  });

  // Legacy link on the Employee record.
  if (!holidayListNames.size && employee.value.holiday_list) {
    holidayListNames.add(employee.value.holiday_list);
  }

  if (!isEmployee.value) {
    // Admin/HR: also gather holiday lists used by active employees.
    try {
      const employees = await getList("Employee", {
        fields: ["name", "holiday_list"],
        filters: [["status", "=", "Active"]],
        limit: 1000,
      });
      employees.forEach((item) => {
        if (item.holiday_list) holidayListNames.add(item.holiday_list);
      });
    } catch (error) {
      console.warn("Could not retrieve employee holiday lists:", error);
    }
  }

  holidays.value = await fetchUpcomingHolidays(holidayListNames);

  // Always fall back to the Holiday Lists stored in the Frappe backend
  // when the assigned lists are missing or have no upcoming holidays.
  if (!holidays.value.length) {
    const backendNames = await getAllHolidayListNames();
    if (backendNames.length) {
      holidays.value = await fetchUpcomingHolidays(backendNames);
    }
  }
}

/* -------------------------------------------------------
   ADMIN / HR DATA FOR SELECTED RANGE
------------------------------------------------------- */
async function loadAdminDashboard() {
  const start = startDate.value;
  const end = endDate.value;

  const results = await Promise.allSettled([
    getCount("Employee"),
    getCount("Department"),

    getCount("Attendance", [
      ["attendance_date", ">=", start],
      ["attendance_date", "<=", end],
      ["status", "=", "Present"],
      ["docstatus", "=", 1],
    ]),

    getCount("Attendance", [
      ["attendance_date", ">=", start],
      ["attendance_date", "<=", end],
      ["status", "=", "Absent"],
      ["docstatus", "=", 1],
    ]),

    getList("Leave Application", {
      fields: ["name", "employee", "leave_type", "from_date", "to_date", "status", "docstatus"],
      filters: rangeOverlapFilters("from_date", "to_date"),
      orderBy: "from_date desc",
      limit: 1000,
    }),

    getCount("Attendance", [
      ["attendance_date", ">=", start],
      ["attendance_date", "<=", end],
      ["docstatus", "=", 1],
    ]),

    getList("Salary Slip", {
      fields: ["name", "employee", "net_pay", "gross_pay", "start_date", "end_date", "docstatus"],
      filters: [
        ["docstatus", "=", 1],
        ["start_date", "<=", end],
        ["end_date", ">=", start],
      ],
      orderBy: "start_date desc",
      limit: 1000,
    }),
  ]);

  const value = (index, fallback = null) =>
    results[index].status === "fulfilled" ? results[index].value : fallback;

  metrics.value.employees = value(0, 0);
  metrics.value.departments = value(1, 0);
  metrics.value.present = value(2, 0);
  metrics.value.absent = value(3, 0);

  adminLeaveApplications.value = value(4, []);
  metrics.value.pendingLeaves = adminLeaveApplications.value.filter((leave) =>
    ["Open", "Pending", "Draft"].includes(String(leave.status || ""))
  ).length;

  metrics.value.attendanceRecords = value(5, 0);
  adminSalarySlips.value = value(6, []);
  metrics.value.salarySlips = adminSalarySlips.value.length;
  metrics.value.payroll = adminSalarySlips.value.reduce(
    (total, slip) => total + Number(slip.gross_pay || 0),
    0
  );

  await loadHolidays();
}

async function loadAdminEmployeeCheckins() {
  employeeCheckinError.value = "";

  try {
    const records = await getList("Employee Checkin", {
      fields: ["employee", "employee_name", "time", "log_type"],
      filters: [
        ["time", ">=", `${startDate.value} 00:00:00`],
        ["time", "<=", `${endDate.value} 23:59:59`],
      ],
      orderBy: "time asc",
      limit: 1000,
    });

    const checkinsByEmployeeAndDate = new Map();

    for (const record of records) {
      if (!record.employee || !record.time) continue;

      const date = String(record.time).slice(0, 10);
      const key = `${record.employee}|${date}`;
      let checkin = checkinsByEmployeeAndDate.get(key);

      if (!checkin) {
        checkin = {
          employee: record.employee,
          employee_name: record.employee_name || record.employee,
          date,
          check_in: "",
          check_out: "",
        };
        checkinsByEmployeeAndDate.set(key, checkin);
      }

      if (record.log_type === "IN" && (!checkin.check_in || record.time < checkin.check_in)) {
        checkin.check_in = record.time;
      } else if (record.log_type === "OUT" && record.time > checkin.check_out) {
        checkin.check_out = record.time;
      }
    }

    adminEmployeeCheckins.value = [...checkinsByEmployeeAndDate.values()].sort(
      (a, b) => b.date.localeCompare(a.date) || a.employee_name.localeCompare(b.employee_name)
    );
  } catch (error) {
    console.warn("Could not load employee check-in records:", error);
    adminEmployeeCheckins.value = [];
    employeeCheckinError.value = t("Could not load employee check-in records. Check your permissions and retry.");
  }
}

/* -------------------------------------------------------
   APPLY / RESET GLOBAL DATE FILTER
------------------------------------------------------- */
async function applyDateFilter() {
  if (!validateDateRange()) return;

  dateLoading.value = true;
  errorMessage.value = "";

  try {
    // Apply the same range to every date-based section.
    if (isEmployee.value) {
      await loadEmployeeDashboard();
    } else {
      await loadAdminDashboard();
      if (isHR.value) {
        await loadAdminEmployeeCheckins();
      }
    }
    filterApplied.value = true;
  } catch (error) {
    console.error("Could not apply date range:", error);
    errorMessage.value = error.message || t("Unable to load data for this date range.");
  } finally {
    dateLoading.value = false;
  }
}

async function resetDate() {
  startDate.value = todayISO;
  endDate.value = todayISO;
  filterError.value = "";
  await applyDateFilter();
}

/* -------------------------------------------------------
   GPS / ATTENDANCE
------------------------------------------------------- */
function getCurrentLocation() {
  return new Promise((resolve, reject) => {
    if (!navigator.geolocation) {
      reject(new Error(t("Your browser does not support location access.")));
      return;
    }

    navigator.geolocation.getCurrentPosition(
      (position) => {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        if (!Number.isFinite(latitude) || !Number.isFinite(longitude)) {
          reject(new Error(t("The browser returned invalid GPS coordinates.")));
          return;
        }

        resolve({ latitude, longitude });
      },
      (error) => {
        const messages = {
          1: t("Location permission denied. Allow location access in browser settings."),
          2: t("Your location is unavailable. Enable device location and try again."),
          3: t("The location request timed out. Please try again."),
        };

        reject(new Error(messages[error.code] || t("Could not access your current location.")));
      },
      { enableHighAccuracy: true, timeout: 20000, maximumAge: 0 }
    );
  });
}

function getLocalDateTime() {
  const now = new Date();
  const pad = (number) => String(number).padStart(2, "0");
  return `${now.getFullYear()}-${pad(now.getMonth() + 1)}-${pad(now.getDate())} ${pad(now.getHours())}:${pad(now.getMinutes())}:${pad(now.getSeconds())}`;
}

function showAttendanceMessage(message, type = "success") {
  if (attendanceMessageTimer) clearTimeout(attendanceMessageTimer);

  attendanceMessageType.value = type;
  attendanceMessage.value = message;

  attendanceMessageTimer = setTimeout(() => {
    attendanceMessage.value = "";
    attendanceMessageTimer = null;
  }, 3000);
}

async function recordCheckin() {
  if (
    !employee.value.name ||
    checkinLoading.value ||
    locationLoading.value ||
    loading.value
  ) return;

  if (!rangeIncludesToday.value) {
    showAttendanceMessage(t("Include today in the date range to record attendance."), "error");
    return;
  }

  const logType = isCheckedIn.value ? "OUT" : "IN";
  const actionLabel = logType === "IN" ? "check-in" : "check-out";

  if (attendanceMessageTimer) clearTimeout(attendanceMessageTimer);
  attendanceMessage.value = "";
  locationLoading.value = true;

  try {
    const { latitude, longitude } = await getCurrentLocation();
    locationLoading.value = false;
    checkinLoading.value = true;

    await frappeRequest("/api/resource/Employee%20Checkin", {
      method: "POST",
      body: JSON.stringify({
        employee: employee.value.name,
        time: getLocalDateTime(),
        log_type: logType,
        latitude,
        longitude,
      }),
    });

    showAttendanceMessage(
      t(`${logType === "IN" ? "Check-in" : "Check-out"} recorded successfully.`),
      "success"
    );

    await loadEmployeeDashboard();
  } catch (error) {
    console.error("Attendance action failed:", error);
    showAttendanceMessage(`${t("Could not record")} ${t(actionLabel)}: ${t(error.message)}`, "error");
  } finally {
    locationLoading.value = false;
    checkinLoading.value = false;
  }
}

/* -------------------------------------------------------
   INITIAL DASHBOARD LOAD
------------------------------------------------------- */
async function loadDashboard() {
  if (loading.value) return;

  loading.value = true;
  errorMessage.value = "";

  try {
    await getLoggedInUser();

    // On first entry, startDate and endDate both default to today.
    startDate.value = todayISO;
    endDate.value = todayISO;

    if (isEmployee.value) {
      await loadEmployeeDashboard();
    } else {
      await loadAdminDashboard();
      if (isHR.value) {
        await loadAdminEmployeeCheckins();
      }
    }
    await loadNotifications();
    filterApplied.value = true;
  } catch (error) {
    console.error("HRMS dashboard error:", error);
    errorMessage.value = error.message || t("Unable to load the dashboard.");
  } finally {
    loading.value = false;
  }
}

onMounted(() => {
  loadWorkspaceMenu();
  loadDashboard();
  document.addEventListener("pointerdown", handleLanguagePickerClickOutside);

  notificationTimer = setInterval(() => {
    if (!notificationsOpen.value) loadNotifications();
  }, 60000);
});

onBeforeUnmount(() => {
  if (attendanceMessageTimer) clearTimeout(attendanceMessageTimer);
  if (notificationTimer) clearInterval(notificationTimer);
  document.removeEventListener("pointerdown", handleLanguagePickerClickOutside);
});
</script>

<style scoped>
.attendance-message-enter-active,
.attendance-message-leave-active {
  transition: opacity 0.2s ease, transform 0.2s ease;
}

.attendance-message-enter-from,
.attendance-message-leave-to {
  opacity: 0;
  transform: translateY(-4px);
}

input[type="date"] {
  color-scheme: light;
}
</style>
