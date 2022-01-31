if (!grepl("modelScripts", getwd())) {
  setwd("liverScripts/modelScripts")
}

reperfusion <- data.table::fread("../results/resultsReperfusionPoolLessHypox.csv")
shortreperfusion <- reperfusion[reperfusion$t < 200, ]

pdf("../dataVis/ischemiaLessHypoxia.pdf", width = 15)
par(mfrow = c(1, 4), cex.axis = 2, cex.lab = 2.5, mar = c(5.1, 5, 4.1, 3))

dpH <- -0.059*log(shortreperfusion$H_x/shortreperfusion$H_i)*1000

plot(shortreperfusion$t, shortreperfusion$NADH_x/4.85e-3, ylim = c(0, 1), cex = 0.1, col = "red",
     xlab = "Time (s)", ylab = "Proportion of the NADH/NAD+ Pool in Reduced State")
lines(shortreperfusion$t, shortreperfusion$NADH_x/4.85e-3, col = "red")

plot(shortreperfusion$t, shortreperfusion$QH2_x/6.49e-3, ylim = c(0, 1), cex = 0.1, col = "red",
     xlab = "Time (s)", ylab = "Proportion of the Coenzyme Q Pool in Reduced State")

plot(shortreperfusion$t, shortreperfusion$dPsi+dpH, cex = 0.1, col = "red", xlab = "Time (s)", 
     ylab = "Proton Motive Force (mV)")

plot(shortreperfusion$t, 1000*shortreperfusion$SUC_x, cex = 0.1, col = "red", xlab = "Time (s)",
     ylab = "Matrix Succinate (mM)")
lines(shortreperfusion$t, 1000*shortreperfusion$SUC_x, col = "red")
dev.off()
